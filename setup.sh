pip3 install -r requirements.txt
echo "place here bot id "
read var_bot_id
echo $var_bot_id > bot_id
echo "place here your telegram username "
read var_username
echo $var_username > creator
ln -s /home/projects/watch_bot/watch_bot.service /etc/systemd/system/watch_bot.service
systemctl enable watch_bot.service
systemctl start watch_bot.service