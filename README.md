# telegram-team-calendar-bot
 A dockerized telegram bot for team planning.

# Pre-reqs
- Go to BotFather on Telegram and create a Bot.
- Please have Docker installed.
- Please create a {NAME}.env environment file with the following information <br>
    TOKEN={YOUR_TOKEN} <br>
    TeamChatId={YOURTEAMCHATID}
- Add the newly created Bot to a group and make him Admin. Afterwhich, type a message in the group.
- ChatId can be retrieved under https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates, Ctrl + F "chatid" 

# To set it up via Docker, run the following commands:
docker build -t {YOUR_IMAGE_NAME} ./ &&
docker run -p 8051:8051 --env-file {NAME}.env {YOUR_IMAGE_NAME} 

# Using the Bot
- Use /dates to choose dates.
- Use /remove to remove dates.
- Use /status to check everyone's availability
- Use /removeKB to remove keyboard symbol
- Use /finalise to view the best date for everyone.
- Use /currentUsers to view everyone in the votes.

