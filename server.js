const express = require("express");
const app = express();

// Allow port/token to be configured through environment variables.
const PORT = process.env.PORT || 80; // oder 443 mit HTTPS
const TOPGG_AUTH = process.env.TOPGG_AUTH; // exakt derselbe Token wie auf top.gg

// Express has built-in JSON body parsing.
app.use(express.json());

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
