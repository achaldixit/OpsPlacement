import os
from server import app


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 6969))
	app.run(host='0.0.0.0', port=port, debug = True)