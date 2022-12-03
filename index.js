import { searchWord } from './functions.js';
import puppeteer from 'puppeteer-core';
import prompts from 'prompts';
import axios from 'axios';
import random from 'random';
import fs from 'fs';

await import('./settings.json', {assert: {type: "json"}}).then(module => {
    global.settings = module.default;
}).catch(err=> {
    if (err.code == 'ERR_MODULE_NOT_FOUND') {
        fs.writeFileSync('./settings.json', JSON.stringify({
            "nickname": "JhonDoe",
            "headless": true,
            "autoMode": false,
            "language": "spanish",
            "max": 30,
            "row": 5
        }, null, 4));
        console.log('settings.json created with default settings, exiting...');
        process.exit(1);
    } else {
        console.error(err);
        process.exit(1);
    }
})

var dict = [];
var wordsList = [];
var word = '';
var lastWord = '';
var currentPlayer = '';

console.clear();
console.log('Getting dictionary...');
await axios.request({
    method: 'GET',
    url: 'https://textic.github.io/assets/dictionary.json',
}).then(res => {
    dict = res.data[settings.language];
}).catch(err => {
    console.log(err);
    process.exit(1);
});
console.log('Dictionary loaded!');

async function main() {
    console.clear();
    const code = await prompts({
        type: 'text',
        name: 'value',
        message: 'Enter the room code',
    });
    const browser = await puppeteer.launch({headless: settings.headless, channel: 'chrome'});
    const page = await browser.newPage();
    await page.goto('https://jklm.fun/');
    await page.evaluate((nickname) => {
        localStorage.setItem('jklmSettings', JSON.stringify({
            "version": 2,
            "volume": 0,
            "muted": false,
            "chatFilter": [],
            "nickname": nickname
        })); 
    }, settings.nickname); // Here is defined the nickname
    console.clear();
    await page.goto('https://jklm.fun/' + code.value);
    console.log('Waiting for iframe...');
    await page.waitForSelector('iframe');
    console.clear();
    const elementHandle = await page.$('iframe');
    const frame = await elementHandle.contentFrame();
    console.log('Waiting for text...');
    await frame.waitForSelector('.syllable');
    console.clear();
    console.log('Game started!');
    if (!settings.autoMode) {
        while (true) {
            word = await frame.$eval('.syllable', el => el.innerText);
            if (word != lastWord && word != '') {
                console.clear();
                console.log('\x1b[38;2;0;255;255mWords:');
                lastWord = word;
                wordsList = searchWord(dict, word, settings.max, settings.mode);
                for (var i = 0; i < wordsList.length; i++) {
                    if (i % settings.row == 0) {
                        console.log('');
                    }
                    process.stdout.write('\x1b[37m' + wordsList[i] + '\x1b[38;2;0;255;255m  |  ');
                }
            }
        }
    } else if (settings.autoMode) {
        console.clear();
        console.log('\x1b[31mAuto mode enabled!');
        var joinBtn = await frame.$('.joinRound');
        var input = await frame.$('.styled');
        while (true) {
            currentPlayer = await frame.$eval('.player', el => el.innerText);
            try { await joinBtn.click() } catch (err) {}
            if (currentPlayer == settings.nickname) {
                word = await frame.$eval('.syllable', el => el.innerText);
                wordsList = searchWord(dict, word, settings.max, settings.mode);
                await input.type(random.choice(wordsList));
                await input.press('Enter');
            }
        }
    } else {
        console.error('Mode must be true or false');
        process.exit(1);
    }
};

main();