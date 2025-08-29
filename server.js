const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const PORT = 80;                 // oder 443 mit HTTPS

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
