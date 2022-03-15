# home assistant configurations
host = "localhost"
port = 8123
token = "xxx"

# Flash configurations
serve_port = 8060
flask_debug = True
route_path = "/hass/bridge"
# if you deploy this flask service behind a reverse-proxy of a web-server (e.g. nginx),
# leave the following two paths empty, and then configure ssl in your web-server's configuration.
ssl_fullchain_pem_path = None
ssl_private_pem_path = None
# ssl_fullchain_pem_path = "/home/ssl/fullchain.pem"
# ssl_private_pem_path = "/home/ssl/privkey.pem"
read_onlys = {
    "名称": ("entity id", "单位"),
}
## on-off devices, e.g. light, switch, script, or anything that can be operated with `homeassistant.turn_on/turn_off`
onoffs = {
    "名称": "entity id",
}
## cover type devices, open/close/stop/set_position
covers = {
    "名称": "entity id",
}

cmd_words_query = ["查一下", "报一下", "当前", "是多少"]
cmd_words_turnon = ["打开", "开一下"]
cmd_words_turnoff = ["关闭", "关上"]
cmd_words_cover_open = ["打开", "升起"]
cmd_words_cover_close = ["关上", "关闭", "降下"]
cmd_words_cover_stop = ["停止"]
cmd_words_cover_setpos = ["一半", "百分之"]
