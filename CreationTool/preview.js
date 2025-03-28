// @ts-check

/**
 * Running this file will preview the EVT file in the terminal
 * It is reccomended to run this in a standalone terminal.
 * Note that the terminal history *will* be cleared.
 */

/**
 * @typedef Data
 * @prop {Record<string, any>} Objects
 * @prop {Record<string, any>} Commands
 * @prop {number} Duration
 */

/** @type {Data} */
// @ts-ignore file too big to get types
const data = require("../P5REssentials/CPK/APPLE.CPK/EVENT/E100/E100/E100_000.evt.json")
const x = 24;
const y = 18;


/** @param {string} input */
function printFrame(input) {
    return new Promise((res, rej) => {
        setTimeout(() => {
            console.clear()
            console.log(input)
            res(null);
        }, 1000 / 20);
    })
}

const objects = new Map(data.Objects.filter(o => o.Type === "Item").map(o => [o.Id.toString(), "0"]))

const frames = data.Commands.filter(c => c.Type === "MAlp")
async function letsGooooo() {
    let frame = 0;
    do {
        const cmds = frames.filter(f => f.Frame === frame)
        for (const cmd of cmds) {
            objects.set(cmd.ObjectId.toString(), cmd.Data.AlphaLevel === 0 ? " " : "0")
        }
        const lines = []
        const vals = [...objects.values()]
        for (let i = 0; i < y; i++) {
            lines.push(vals.slice(i * x, (i + 1) * x).join(" "))
        }
        await printFrame(lines.join("\n"))
        frame++;
    } while (frame < data.Duration);
}

letsGooooo();