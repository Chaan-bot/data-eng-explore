<!--  Daily docker cmds -->

docker compose up -d # start
docker compose down # stop (data survives)
docker compose down -v # stop AND delete all data
docker compose logs -f db # tail the log
docker compose exec db psql -U dex -d dex # psql shell
