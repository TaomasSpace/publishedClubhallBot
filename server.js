const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const app = express();
// Allow port/token to be configured through environment variables.
const PORT = process.env.PORT || 80; // oder 443 mit HTTPS

const fs = require("fs");

const TOPGG_AUTH = fs.readFileSync("topgg.txt", "utf8").trim();
// Express has built-in JSON body parsing.
app.use(express.json());

app.post("/vote", (req, res) => {
    const auth = req.header("Authorization");
    if (auth !== TOPGG_AUTH) {
        return res.status(403).send("Invalid token");
    }
    const user = String(req.body.user);
    const script = path.join(__dirname, "scripts", "award_vote.py");
    const child = spawn("python", [script, user]);
    child.stdout.on("data", data => {
        const reward = data.toString().trim();
        console.log(`User ${user} voted and received ${reward} coins.`);
    });
    child.on("error", err => {
        console.error(err);
        res.status(500).send("Script error");
    });
    child.on("close", code => {
        if (code === 0) {
            res.sendStatus(200);
        } else {
            res.status(500).send("Script error");
        }
    });
});

app.listen(PORT, () => console.log(`Webhook läuft auf Port ${PORT}`));
