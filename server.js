const https = require("https");
const fs = require("fs");
const express = require("express");
const app = express();
app.use(bodyParser.json());               // oder 443 mit HTTPS

const TOPGG_AUTH = "lS6lvCvcDdDKklWoUHLLjtz10g0eZCW8"; // exakt derselbe Token wie auf top.gg

app.use(bodyParser.json());

app.post("/vote", (req, res) => {
    const auth = req.header("Authorization");
    if (auth !== TOPGG_AUTH) {
        return res.status(403).send("Invalid token");
    }
    const { user, type } = req.body;  // {"user":"123456789","type":"upvote",...}
    console.log(`User ${user} hat für deinen Bot gestimmt! Typ: ${type}`);
    // => hier z.B. Belohnungen verteilen, Datenbank aktualisieren, etc.
    res.sendStatus(200);
});

app.listen(PORT, () => console.log(`Webhook läuft auf Port ${PORT}`));

const options = {
    key: fs.readFileSync("/etc/letsencrypt/live/clubhallbot.duckdns.org/privkey.pem"),
    cert: fs.readFileSync("/etc/letsencrypt/live/clubhallbot.duckdns.org/fullchain.pem")
};
https.createServer(options, app).listen(443, () =>
    console.log("HTTPS‑Webhook läuft auf Port 443")
);