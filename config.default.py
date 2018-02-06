# home assistant configurations
host = "localhost"
port = 8123
password = "xxxx"

# Flash configurations
serve_port = 18443
flask_debug = True
route_path = "/hass/dev"
# if you deploy this flask service behind a reverse-proxy of a web-server (e.g. nginx),
# leave the following two paths empty, and then configure ssl in your web-server's configuration.
ssl_fullchain_pem_path = None
ssl_private_pem_path = None
# ssl_fullchain_pem_path = "/home/ssl/fullchain.pem"
# ssl_private_pem_path = "/home/ssl/privkey.pem"

# skill configurations
skill_name = "大卫"
## read-only devices/attributes
read_onlys = {
    "室内光强": ("sensor.illumination_34ce0088e3bc", "流明"),
    "室外光强": ("sensor.lux_sensor", "拉克丝"),
    "室内温度": ("sensor.temperature_158d000170d469", "度"),
    "室外温度": ("sensor.dht_sensor_temperature", "度"),
    "室内湿度": ("sensor.humidity_158d000170d469", ""),
    "室外湿度": ("sensor.dht_sensor_humidity", "")
}
## on-off devices, e.g. light, switch, script, or anything that can be operated with `homeassistant.turn_on/turn_off`
onoffs = {
    "餐厅灯": "light.diningroom_light",
    "厨房灯": "light.kitchen_light",
    "阳台灯": "light.balcony_light",
    "卧室灯": "light.bedroom_main_light",
    "卧室阅读灯": "switch.yishang_light",
    "所有卧室灯": "group.bedroom_lightst",
    "所有客厅灯": "group.livingroom_lights"
}
## cover type devices, open/close/stop/set_position
covers = {
    "窗帘": "cover.dooyacurtain",
    "卷帘": "cover.dooyaroller",
    "晾衣架": "cover.clothes_dryer"
}

cmd_words_query = ["查一下", "报一下", "当前", "是多少"]
cmd_words_turnon = ["打开", "开一下"]
cmd_words_turnoff = ["关闭", "关上"]
cmd_words_cover_open = ["打开", "升起"]
cmd_words_cover_close = ["关上", "关闭", "降下"]
cmd_words_cover_stop = ["停止"]
cmd_words_cover_setpos = ["一半", "百分之"]

