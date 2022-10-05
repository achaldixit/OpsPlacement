import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages
import pandas as pd

base = importr("base")
utils = importr("utils")
rxl = importr("readxl")
utils.chooseCRANmirror(ind=45)

packages = ["tidyverse", "readxl","writexl", "geodist", "ompr", "ompr.roi", "ROI.plugin.symphony", "ggrepel", "fields", "ROI.plugin.glpk", "DBI", "magrittr"
]
# Selectively install what needs to be install.
# We are fancy, just because we can.
names_to_install = [x for x in packages if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
  utils.install_packages(StrVector(names_to_install))

ompr = importr("ompr")
roi = importr("ompr.roi")
symphony = importr("ROI.plugin.symphony")
tidy = importr("tidyverse")

robjects.r(''' 

dummy <- function(){
set.seed(1234)

grid_size <- 1000


params <- read_csv("model_params.txt")
inflation_factor <- params$params[2]
carting_cost <- params$params[3]
truck_cost <- params$params[4]


n <- 100 * inflation_factor
customer_locations <- data.frame(
  id = 1:n,
  x = round(runif(n) * grid_size),
  y = round(runif(n) * grid_size)
)
m <- 20
warehouse_locations <- data.frame(
  id = 1:m,
  x = round(runif(m) * grid_size),
  y = round(runif(m) * grid_size)
)

fixedcost <- round(rnorm(m, mean = grid_size * 10, sd = grid_size * 5))

transportcost <- function(i, j) {
  customer <- customer_locations[i, ]
  warehouse <- warehouse_locations[j, ]
  distance <-
    round(sqrt((customer$x - warehouse$x) ^ 2 + (customer$y - warehouse$y) ^ 2))
  carting <- distance * carting_cost * 1000
  return(cost)
}


model <- MIPModel() %>%
  # 1 iff i gets assigned to warehouse j
  add_variable(x[i, j], i = 1:n, j = 1:m, type = "binary") %>%
  
  # 1 iff warehouse j is built
  add_variable(y[j], j = 1:m, type = "binary") %>%
  
  # maximize the preferences
  set_objective(sum_expr(transportcost(i, j) * x[i, j], i = 1:n, j = 1:m) + 
                  sum_expr(fixedcost[j] * y[j], j = 1:m), "min") %>%
  
  # every customer needs to be assigned to a warehouse
  add_constraint(sum_expr(x[i, j], j = 1:m) == 1, i = 1:n) %>% 
  
  # if a customer is assigned to a warehouse, then this warehouse must be built
  add_constraint(x[i,j] <= y[j], i = 1:n, j = 1:m)
model

result <- solve_model(model, with_ROI(solver = "symphony"))

matching <- result %>% 
  get_solution(x[i,j]) %>%
  filter(value > .9) %>%  
  select(i, j)

plot_assignment <- matching %>% 
  inner_join(customer_locations, by = c("i" = "id")) %>% 
  inner_join(warehouse_locations, by = c("j" = "id"))

customer_count <- matching %>% group_by(j) %>% summarise(n = n()) %>% rename(id = j)

plot_warehouses <- warehouse_locations %>% 
  mutate(costs = fixedcost) %>% 
  inner_join(customer_count, by = "id") %>% 
  filter(id %in% unique(matching$j))

print("Saving Model Graph")

png("/Users/delhivery/Documents/Hackathons/OpsPlacement/server/static/plot.png", width = 800, height = 600)

p <- ggplot(customer_locations, aes(x, y)) + 
  geom_point() + 
  geom_point(data = warehouse_locations, color = "red", alpha = 0.5, shape = 17) +
  scale_x_continuous(limits = c(0, grid_size)) +
  scale_y_continuous(limits = c(0, grid_size)) +
  theme(axis.title = element_blank(), 
        axis.ticks = element_blank(), 
        axis.text = element_blank(), panel.grid = element_blank())
p <- p + 
  geom_segment(data = plot_assignment, aes(x = x.y, y = y.y, xend = x.x, yend = y.x)) + 
  geom_point(data  = plot_warehouses, color = "red", size = 3, shape = 17) +
  ggrepel::geom_label_repel(data  = plot_warehouses, 
                            aes(label = paste0("fixed costs:", costs, "; customers: ", n)), 
                            size = 2, nudge_y = 20) + 
  ggtitle(paste0("Cost optimal locations and pincodes assignment"))
plot(p)
dev.off()
print("Graph Saved")
}
dummy()
''')