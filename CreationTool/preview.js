// @ts-check

/**
 * Running this file will preview the EVT file in the terminal
 * It is reccomended to run this in a standalone terminal.
 * Note that the terminal history *will* be cleared.
 */

/**
 * 
 * @typedef EVTObject
 * @prop {number} Id
 * @prop {string} Type
 * @prop {number} Field08
 * @prop {number} Field0C
 * @prop {number} ResourceMajorId
 * @prop {number} ResourceSubId
 * @prop {number} ResourceMinorId
 * @prop {number} Field1C
 * @prop {number} AnimationMajorId
 * @prop {number} AnimationMinorId
 * @prop {number} AnimationSubId
 * @prop {number} Field28
 * @prop {number} Field2C
 * 
 * @typedef EVTCommand
 * @prop {string} Type
 * @prop {number} Field04
 * @prop {number} Field06
 * @prop {number} ObjectId
 * @prop {number} Field0C
 * @prop {number} Frame
 * @prop {number} Duration
 * @prop {number} DataSize
 * @prop {string} EvtFlagType
 * @prop {number} EvtFlagId
 * @prop {number} EvtFlagValue
 * @prop {string} EvtFlagConditionalType
 * @prop {Record<string, any>} Data
 * 
 * @typedef Data
 * @prop {EVTObject[]} Objects
 * @prop {Record<string, any>[]} Commands
 * @prop {number} Duration
 */

/** @type {Data} */
// @ts-ignore file too big to get types
const data = require("../P5REssentials/CPK/APPLE.CPK/EVENT/E100/E100/E100_000.evt.json")
const x = 24;
const y = 18;
const fps = 24


/** @param {string} input */
function printFrame(input) {
    return new Promise((res, rej) => {
        setTimeout(() => {
            console.clear()
            console.log(input)
            res(null);
        }, 1000 / fps);
    })
}

const objects = new Map(data.Objects.filter(o => o.Type === "Item").map(o => [o.Id.toString(), "0"]))

const frames = data.Commands.filter(c => c.Type === "MAlp")

async function letsGooooo() {
    for (let frame = 0; frame < data.Duration; frame++) {
        const cmds = frames.filter(f => f.Frame === frame)
        for (const cmd of cmds) {
            objects.set(cmd.ObjectId.toString(), cmd.Data.AlphaLevel === 0 ? " " : "0")
        }
        const lines = []
        const vals = [...objects.values()]
        for (let i = y - 1; i >= 0; i--) {
            lines.push(vals.slice(i * x, (i + 1) * x).join(" "))
        }
        await printFrame(lines.join("\n"))
    }
}

letsGooooo();