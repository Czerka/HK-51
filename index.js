require('dotenv').config()

const fs = require('fs')
const path = require('path')
const exec = require('child_process').exec

const Discord = require("discord.js")
const client = new Discord.Client()

let LAST_DATE = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '')

client.on('ready', async () => {
    console.log(`Logged in as ${client.user.tag}!`)

    client.user.setActivity('with meatbags', {
        type: 'PLAYING',
    });

    console.log('Looking at twitter...')

    let channel = await (await client.guilds.fetch(process.env.DISCORD_SERVER)).channels.resolve(process.env.DISCORD_CHANNEL)
    channel.send(process.env.DISCORD_UP_MESSAGE)
    channel.send(process.env.DISCORD_UP_MESSAGE_2)

    setInterval(async () => {
        tweets = await readTweets(LAST_DATE).catch(console.log)
        tweets.forEach(tweet => {
            console.log(`Sending [${tweet.id}] to Discord!`)
            channel.send('https://twitter.com/SWTOR/status/' + tweet.id)
            LAST_DATE = tweet.timestamp
        })
    }, 5 * 60 * 1000);
})

client.login(process.env.DISCORD_TOKEN)

// ----- FUNCTIONS ----- //
async function readTweets(lastDate) {
    await run('python ' + path.join(__dirname, 'main.py') + ' "' + lastDate + '"')

    let filepath = path.join(__dirname, 'ids.txt')
    let content = fs.readFileSync(filepath, 'utf-8')
    let tweets = content.split('\n').slice(0, -1)
    return tweets.map(tweet => {
        let parts = tweet.split('\t')
        return {
            id: parts[0],
            timestamp: parts[1].slice(0, 19)
        }
    }).sort((a, b) => a.timestamp < b.timestamp ? -1 : 1)
}

function run(cmd) {
    return new Promise((resolve, reject) => {
        exec(cmd, (error, stdout, stderr) => {
            if (error) reject({ message: error.message, log: stderr })
            resolve()
        })
    })
}
