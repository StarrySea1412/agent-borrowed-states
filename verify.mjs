import { createRequire } from "node:module";
const require = createRequire("D:/project/git-primer/node_modules/");
const { chromium } = require("playwright-core");

const results = [];
const check = (name, cond) => results.push([cond ? "PASS" : "FAIL", name]);
const errors = [];

const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });
page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
page.on("console", (m) => { if (m.type() === "error") errors.push("console.error: " + m.text()); });

await page.goto("http://127.0.0.1:8093/", { waitUntil: "networkidle" });

/* ---------- DEMO 01 · 五步时间线 ---------- */
await page.locator("#d1").scrollIntoViewIfNeeded();
for (let i = 0; i < 5; i++) await page.click("#d1-next");
check("d1 五步后消息去向=两头落空", (await page.textContent("#d1-rr")) === "两头落空");
check("d1 网关B=运行 · :37289", (await page.textContent("#d1-rb")).includes("37289"));
check("d1 日志含 chat-transport 警告", (await page.textContent("#d1-log")).includes("chat-transport"));
check("d1 下一步已禁用", await page.locator("#d1-next").isDisabled());
await page.click("#d1-reset");
check("d1 重置后读数复位", (await page.textContent("#d1-rr")) === "——");

/* ---------- DEMO 02 · 四幕 + 手术 ---------- */
await page.locator("#d2").scrollIntoViewIfNeeded();
await page.click("#d2-play");
await page.waitForFunction(() => document.getElementById("d2-verdict").textContent.includes("拒绝启动"), null, { timeout: 9000 });
check("d2 四幕后结论=拒绝启动（假活）", (await page.textContent("#d2-verdict")).includes("拒绝启动"));
check("d2 日志含 lock timeout 报文", (await page.textContent("#d2-log")).includes("lock timeout after 5000ms"));
check("d2 6240 易主 WMI 服务", (await page.textContent("#d2-who")).includes("WMIRegistrationService"));
await page.waitForFunction(() => !document.getElementById("d2-verdict").textContent.includes("等待"), null, { timeout: 3000 }).catch(() => {});
await page.click("#d2-surg");
check("d2 手术后僵尸行=已摘除", (await page.textContent("#d2-zombie")) === "已摘除");
check("d2 手术后结论=ready ✓", (await page.textContent("#d2-verdict")) === "ready ✓");
await page.click("#d2-reset");
check("d2 重置后结论复位", (await page.textContent("#d2-verdict")) === "——");

/* ---------- DEMO 03 · 200 测活闸 ---------- */
await page.locator("#d3").scrollIntoViewIfNeeded();
await page.click("#d3-test");
check("d3 默认闸A=通过（现状复现）", (await page.textContent("#d3-verdict")).includes("通过"));
await page.$eval("#d3-gateB", (n) => { n.checked = true; n.dispatchEvent(new Event("change")); });
await page.click("#d3-test");
check("d3 开闸B后=失败（检测到拒绝文案）", (await page.textContent("#d3-verdict")).includes("失败"));
check("d3 下游后果阻止接入", (await page.textContent("#d3-after")).includes("阻止接入"));
await page.click("#d3-reset");
check("d3 重置后复位", (await page.textContent("#d3-verdict")) === "——");

/* ---------- DEMO 04 · 31 发重放（实录加速） ---------- */
await page.locator("#d4").scrollIntoViewIfNeeded();
await page.click("#d4-play");
await page.waitForTimeout(2500);
check("d4 无限模式 2.5 秒内已发出多枚", parseInt(await page.textContent("#d4-n")) > 3);
await page.waitForFunction(() => document.getElementById("d4-n").textContent === "31", null, { timeout: 30000 });
check("d4 无限模式最终=31 发", (await page.textContent("#d4-n")) === "31");
check("d4 结束语=实录到 31 发为止", (await page.textContent("#d4-end")).includes("31 发为止"));
await page.click("#d4-reset");
await page.$eval("#d4-bounded", (n) => { n.checked = true; n.dispatchEvent(new Event("change")); });
await page.click("#d4-play");
await page.waitForFunction(() => document.getElementById("d4-n").textContent === "3", null, { timeout: 15000 });
check("d4 有界模式 3 发熔断", (await page.textContent("#d4-end")).includes("3 发后熔断"));
await page.click("#d4-reset");

/* ---------- DEMO 05 · 接入累加器 ---------- */
await page.locator("#d5").scrollIntoViewIfNeeded();
const before = await page.textContent("#d5-states");
await page.click("#d5-add"); await page.click("#d5-add"); await page.click("#d5-add");
check("d5 接三次后层数=4", (await page.textContent("#d5-layers")) === "4");
check("d5 状态总数增加", parseInt(await page.textContent("#d5-states")) > parseInt(before));
await page.click("#d5-remove");
check("d5 卸载后残留=1", (await page.textContent("#d5-residue")) === "1");
check("d5 卸载后层数回落=3", (await page.textContent("#d5-layers")) === "3");
await page.click("#d5-reset");
check("d5 重置后层数=1", (await page.textContent("#d5-layers")) === "1");

/* ---------- 移动端 390px 溢出扫描 ---------- */
await page.setViewportSize({ width: 390, height: 844 });
await page.waitForTimeout(400);
const overflows = await page.$$eval("body *", (els) => {
  const bad = [];
  for (const el of els) {
    if (el.closest(".tbl-wrap")) continue;
    const r = el.getBoundingClientRect();
    if (r.right > 391 && r.width > 0) {
      const tag = el.tagName.toLowerCase();
      if (tag === "svg" || el.querySelector("svg")) continue;
      bad.push(`${tag}.${(el.className || "").toString().slice(0, 30)} right=${Math.round(r.right)}`);
    }
  }
  return bad.slice(0, 12);
});
check("390px 无溢出（" + overflows.length + " 处）", overflows.length === 0);
if (overflows.length) console.log("溢出清单:", JSON.stringify(overflows, null, 1));

/* ---------- 截图目检 ---------- */
await page.setViewportSize({ width: 1200, height: 900 });
for (const id of ["d1", "d2", "d3", "d4", "d5"]) {
  await page.locator("#" + id).scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.locator("#" + id).screenshot({ path: `shot-${id}.png` });
}
await page.screenshot({ path: "shot-hero.png" });

console.log("=== 结果 ===");
let pass = 0;
for (const [s, n] of results) { console.log(s, n); if (s === "PASS") pass++; }
console.log(`${pass}/${results.length} PASS`);
console.log("JS 错误:", errors.length === 0 ? "none" : errors.join(" | "));
await browser.close();
process.exit(pass === results.length && errors.length === 0 ? 0 : 1);
