import yaml

config = {
  "font" : {
    "family" : "Terminal",
    "size" : 10,
    "tabstop" : 4
  },
  "colors" : {
    "bg": "#ffffff",
    "txt": "#000000",
  }
}

def generate_config(path):
  with open(f"{path}", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    for itm in data:
      if itm in config:
        if itm == "colors":
          for col_itm in data["colors"]:
            if col_itm in config["colors"]:
              config[itm][col_itm] = hex(data[itm][col_itm])
              config[itm][col_itm] = config[itm][col_itm].replace("0x", "#")[::-1].zfill(7)[::-1]
        elif itm == "font":
          for fnt in data["font"]:
            if fnt in config["font"]:
              config[itm][fnt] = data[itm][fnt]
            else:
              raise Exception(f"Item {fnt} is not a recognised item.")
      else:
        raise Exception(f"Item {itm} is not a recognised item.")
  return config
