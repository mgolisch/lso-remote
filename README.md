# lso-remote
simple websocket server to control livesplitone

example usage:

1. pip install --user pipx
2. pipx install git+https://github.com/mgolisch/lso-remote
3. lso-remote run-server
4. connect local lso or one.livesplit.org to ws://localhost:5000 (seems to work fine in chromium atleast)
5. send commands using lso-remote send-command (split/skip/reset .. see --help)
6. use hotkey app of choice (DE/WM default or something like https://github.com/baskerville/sxhkd) to bind keys to the corresponding command
7. profit
