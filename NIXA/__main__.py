


import glob
from pathlib import Path
from NIXA.utils import load_plugins
import logging
from NIXA import NIXA

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

path = "NIXA/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
    
print("» sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ...")
print("» ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴛʜᴇsᴇ ᴄʜᴀɴɴᴇʟ @TechQuard")

if __name__ == "__main__":
    NIXA.run_until_disconnected()
