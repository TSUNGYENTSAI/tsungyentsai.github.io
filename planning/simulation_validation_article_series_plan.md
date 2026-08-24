# Simulation / Validation Article Series Plan

Status: 2026-08-24

## Series goal

This series is not meant to document individual simulation projects or specific simulation engines.

The goal is to extract reusable engineering principles from robotics deployment, simulation, warehouse automation, and later decision-system work:

1. What reality should a simulation preserve?
2. Where should simulation connect to the production system?
3. What reality should be deliberately removed?
4. What capabilities should become reusable validation infrastructure?

The progression should move from **simulation fidelity** toward **system architecture and validation infrastructure**, rather than becoming a sequence of AMR case studies.

---

# Article 1 — Published

## Built for Simulation, Not Visualization

**Subtitle**

> Choosing simulation fidelity for the decision you need to make.

**Core question**

> What reality does this decision actually require?

**Core thesis**

> Fidelity follows the decision.

A simulation does not need to preserve every detail of reality. It needs to preserve the mechanisms that matter to the decision being made.

**Cases used**

- FARobot full / partial / mock simulation configurations
- TAC discrete-event simulation
- FARobot deployment throughput improvement
- Sim-to-real positioning error

**Role in the series**

Establishes the abstraction principle.

```text
decision
→ relevant reality
→ required fidelity
```

Do not repeat these cases in full in later articles. Later pieces should reference them only when deriving a new principle.

---

# Article 2 — Final draft

## What Is Your Simulation Actually Testing?

**Subtitle**

> How integration boundaries shape what simulation results can support.

**Core question**

> Where should simulation connect to the production software stack?

**Core thesis**

> The integration boundary determines which production software remains under test, what behavior is substituted, and what claims the resulting evidence can support.

**Main concepts**

### Integration boundary

Which production implementation stays inside the loop?

### System under test

Full-stack, partial-stack, and mock-agent configurations test different software responsibilities.

### Hidden contracts

Adding a second physical-world implementation forces previously implicit assumptions about:

* state ownership
* initialization
* lifecycle
* authoritative updates
* component responsibility

to become explicit.

### Substitute behavior

A substitute can:

* hide failures that exist in production;
* introduce failures that exist only in simulation.

Interface compatibility alone does not guarantee behavioral representativeness.

### Evidence ceiling

What was simulated away places a hard limit on the claims the experiment can support.

Scenario quality and evaluation affect evidence strength, but they cannot recover evidence for production code that never ran.

**Final engineering questions**

* What production code actually ran?
* What did we replace?
* What failures can that substitute hide or create?
* What claim are we trying to support?

**Role in the series**

Moves from modeling abstraction to software architecture:

```text
fidelity
→ integration boundary
→ system under test
→ evidence ceiling
```

---

# Article 3 — Planned

## Working title

### The Simulation I Made Less Real on Purpose

Alternative:

* When Less Simulation Gives a Better Answer
* Removing Reality to Isolate the Decision

Current preference:

> **The Simulation I Made Less Real on Purpose**

## Core question

> When should simulation deliberately remove real system behavior rather than reproduce it?

## Core thesis

More detailed simulation is not always a better experiment.

Sometimes low-level behavior creates variance without helping the decision. Removing it can make competing strategies easier to compare and the resulting evidence easier to interpret.

```text
more reality
≠
better decision signal
```

## Primary case

TAC / ASRS discrete-event simulation.

The important contrast with FARobot:

### FARobot

Simulation acted as a substitute for part of a real software / physical system.

### TAC

Simulation was deliberately reduced to a decision model.

The goal was not to reproduce complete AMR traffic behavior. The goal was to compare storage and allocation decisions under controlled assumptions.

## Reality to preserve

Potentially include:

* orders
* inventory state
* containers
* storage locations / stacks
* stack-locking constraints
* reshuffling / moveback
* workstation demand
* allocation decisions
* relevant time / operation costs

Exact list should be checked against TAC canonical notes before drafting.

## Reality deliberately removed

Most low-level robot traffic / navigation behavior.

Reason:

> It was not the decision being evaluated and could obscure differences between allocation strategies.

## Important technical point

This should not be framed as:

> DES was cheaper than robot simulation.

The stronger argument is:

> Removing robot-level behavior isolated the decision mechanism.

The abstraction was part of experiment design.

## Candidate concrete scar

A simpler heuristic could outperform a more sophisticated-looking policy under the actual system constraints.

Use only examples supported by the TAC record.

The reader should leave with the idea that:

> A model can become more useful by becoming less complete.

## Evaluation discussion

Potential topics:

* repeated stochastic runs
* mean / variance rather than single-run results
* controlled comparison
* keeping decision variables visible
* separating decision signal from operational noise

Do not overstate the model as a throughput guarantee if it was designed primarily for comparative evaluation.

## Ending

Connect Articles 1–3:

```text
Article 1:
What reality matters?

Article 2:
Where should reality be substituted?

Article 3:
What reality should be intentionally removed?
```

Possible closing idea:

> Abstraction is not what remains after fidelity is removed. It is a design decision about which mechanisms deserve to influence the result.

## Inputs to review before writing

* TAC canonical experience record
* exact DES state model
* policies compared
* metrics and statistical treatment
* which robot behaviors were explicitly omitted
* strongest counterintuitive result
* claim / confidentiality boundaries

---

# Article 4 — Planned synthesis

## Working title

Current conceptual title:

### From Simulation Environment to Validation Infrastructure

Possible stronger titles to explore later:

* What I Would Build Into a Robotics Control Platform From Day One
* If I Were Building a Robotics Control System Again
* Beyond the Simulator: Building Robotics Validation Infrastructure
* What Should Survive Beyond the Simulator?

Do not finalize the title yet. The final article may be broader than simulation.

## Core question

> After working on control and simulation systems across two autonomous-material-handling companies, what capabilities would I make reusable if I were building a robotics control platform again?

## Core thesis

The reusable asset is not the simulator.

The reusable asset is the infrastructure that lets the same production system be:

* connected to real robots;
* connected to simulated substitutes;
* reconstructed from field evidence;
* evaluated under controlled scenarios;
* compared across changes;
* regression-tested;
* supported by traceable evidence.

## Important framing

This is a **synthesis / proposed architecture**, not a claim that all of these capabilities existed as a mature platform in previous companies.

Use language such as:

> If I were designing this again...

or:

> Looking across these systems, these are the responsibilities I would separate from the beginning.

Do not rewrite history as though this architecture was formally implemented end-to-end.

---

## Architecture model

Separate two planes.

### A. Runtime / control plane

Domain-dependent production behavior:

```text
Mission / Order
↓
Task allocation
↓
Planning / scheduling
↓
Traffic / resource coordination
↓
Robot command & lifecycle
↓
Robot / equipment interface
```

Exact modules vary by domain.

AMR, UAV, warehouse automation, mobile manipulation, and other autonomy systems should not be forced into one identical control architecture.

### B. Validation / evidence plane

Capabilities that should survive across domains and simulator choices:

```text
System contracts
Operational state
Execution substitution
Scenario
Observability
Evaluation
Regression
Evidence
```

This is the real focus of the article.

---

## Candidate reusable responsibilities

### 1. System contracts and identity

Define explicitly:

* agent / equipment identity
* commands
* task and action lifecycle
* state ownership
* timestamps / correlation IDs
* capability definitions
* errors and recovery semantics

Lesson from deployment:

> Simulation integration becomes difficult when the production system itself cannot clearly state who owns state or when an action is complete.

---

### 2. Operational state / world representation

The system needs a coherent operational representation of:

* agents
* tasks
* resources
* equipment
* topology
* payload / inventory
* reservations
* relevant constraints

Do not argue for one giant universal world model.

A later principle may be:

> Shared reality does not require one shared representation.

Different decisions may require different projections of the same operational reality.

---

### 3. Planning and orchestration

Examples:

* task allocation
* scheduling
* routing
* traffic coordination
* resource assignment
* recovery decisions

This layer is domain-specific and should not dominate the article.

The important architectural property is that its dependencies can be clearly connected to real execution or controlled substitutes.

---

### 4. Execution adapters / substitution layer

Potentially the most distinctive module.

A production control system should not need to know whether an execution dependency is:

```text
real robot
full-stack simulated robot
partial simulated agent
mock agent
replay agent
```

provided that the selected implementation satisfies the relevant contract.

Article 2 provides the important limitation:

> Different substitutes create different evidence ceilings.

Do not imply interchangeability means equivalent validation.

---

### 5. Scenario and experiment infrastructure

Convert:

```text
field incident
→ reproducible scenario

design question
→ counterfactual scenario

known failure
→ regression scenario
```

A scenario may describe:

* initial state
* topology / environment
* agents
* workload / task sequence
* disturbances
* failure injection
* configuration
* random seed
* expected observations

Use FARobot's manual reconstruction workflow as the motivating scar, not as an architecture success story.

---

### 6. Observability, evaluation and evidence

Observability should make execution reconstructable without manually correlating fragmented logs.

Possible structured dimensions:

* task
* action
* agent
* state transition
* resource waiting
* error
* timing
* configuration / software version

Evaluation converts execution into decision evidence:

* throughput
* completion time
* waiting
* utilization
* blocking
* failure / safety events
* recovery behavior
* domain-specific metrics

Evidence artifact should connect:

```text
scenario
+ code/config version
+ run
+ metrics
+ violations
+ comparison
```

This enables:

* regression
* benchmark
* release gates
* deployment decisions

---

## Criteria for what deserves to become infrastructure

A useful higher-level framework:

A capability deserves platform investment when it meets one or more of these conditions:

### Repeated across decisions

It appears in many use cases rather than one algorithm.

### Survives multiple integration boundaries

It is needed whether execution is real, simulated, mocked, or replayed.

### Manual recreation damages evidence quality

Repeated ad-hoc setup makes results difficult to reproduce, compare, or trust.

This prevents the article from becoming a generic list of “modules every robotics company needs.”

---

## Primary experience sources

### FARobot

Provides lessons around:

* real deployment
* FMS / robot integration
* hybrid simulation
* scalability
* state contracts
* field debugging
* manual logs
* scenario reconstruction
* sim-to-real robustness

### TAC

Provides lessons around:

* deliberate abstraction
* experiment design
* controlled comparisons
* stochastic evaluation
* separating decision signal from operational detail

Together they support the synthesis.

---

## Material intentionally moved here from Article 2

Do not lose these notes:

### Field evidence workflow

```text
SSH into systems
→ copy FMS / robot logs
→ txt / zip
→ ticket
→ locate timestamps and task IDs
→ manually correlate modules
→ reconstruct failure
```

Observed problems:

* timestamps not aligned
* logs distributed across ROS nodes
* task IDs difficult to correlate
* no unified event schema
* difficult to reconstruct complete system state

### Scenario reconstruction

Two types:

#### Failure reproduction

Preserve enough task / route / state detail to reproduce a mechanism.

#### Decision / throughput experiment

Exact starting state may not matter; preserve workload, layout, fleet configuration, bottleneck structure and relevant statistics.

Important principle:

> Field evidence is not automatically a scenario.

### Repeatability

* task sequences could be fixed
* outcomes were not deterministic
* multiple runs were sometimes required
* setup still involved substantial manual work

### Routing bug candidate

Right-triangle topology case:

* one direction selected the diagonal;
* the reverse direction selected the two perpendicular edges;
* investigation pointed to inconsistent path-weight behavior.

Before public use:

* verify against personal records;
* record claim provenance;
* avoid unnecessary former-employer implementation detail.

### Deployment experiment loop

```text
hypothesis
→ simulation
→ inspect behavior / metrics
→ deployment discussion
→ field change
→ measurement
→ new evidence
```

Metrics available in one-off analysis included:

* robot idle time
* average task time
* average velocity
* station waiting
* blocking / deadlock count

Important limitation:

> These analysis capabilities were useful but not fully integrated into the FMS product.

This is a strong motivation for reusable validation infrastructure.

### Faster-than-real-time

Preserve this experience for Article 4 rather than Article 2.

Potential lesson:

> Accelerating robot motion is not the same as virtualizing time for a distributed system.

Topics to revisit:

* clock ownership
* time virtualization
* timeout semantics
* message ordering
* action lifecycle
* deterministic / reproducible execution

Do not write until exact implementation details and observed failure modes are reviewed.

---

# Possible later series — not yet committed

## From Digital Twin to Decision Infrastructure

This should probably start a **new series**, rather than become Article 5 of the simulation series.

The simulation series asks:

> How do we build and validate systems that interact with reality?

The later decision-infrastructure series would ask:

> How do we represent reality, encode engineering knowledge, evaluate alternatives, and produce decision evidence even when runtime simulation is not required?

Potential abstraction:

```text
Representation
+
Knowledge / Rules
+
Verification / Evaluation / Search
+
Evidence
```

Possible source material:

* Layout verification / placement
* Hookup routing
* rule grounding
* decision-grade representation
* operational representations
* digital twin discussions

Potential thesis:

> Simulation is one kind of decision engine. A broader decision infrastructure does not require every problem to become a runtime simulation.

### Publication caution

Much of this material comes from current work.

Do not schedule or draft detailed public cases until:

* confidentiality boundaries are clear;
* product strategy is stable enough;
* publication timing with the company / CEO is resolved.

For now, preserve only high-level concepts.

---

# Current publication sequence

```text
1. Built for Simulation, Not Visualization
   [Published]
   What reality matters?
   → Fidelity follows the decision.

2. What Is Your Simulation Actually Testing?
   [Final draft]
   Where does simulation enter the production stack?
   → Integration boundary / system under test / evidence ceiling.

3. The Simulation I Made Less Real on Purpose
   [Planned]
   What reality should be deliberately removed?
   → Decision abstraction / experimental signal.

4. From Simulation Environment to Validation Infrastructure
   [Planned synthesis]
   What capabilities should become reusable infrastructure?
   → Contracts / substitution / scenarios / observability /
     evaluation / regression / evidence.

------------------------------------------------------------

Possible next series:

From Digital Twin to Decision Infrastructure
   How do these ideas generalize beyond runtime simulation?
```

# Writing policy for future articles

Before drafting each article:

1. Re-read the relevant canonical experience records.
2. Separate verified facts from retrospective interpretation.
3. Decide the one new concept the article contributes.
4. Use implementation details only when they provide evidence for that concept.
5. Do not turn a retrospective taxonomy into a claim that the architecture was designed formally from day one.
6. Keep public claims within existing safety / confidentiality boundaries.
7. Write from an English argument outline rather than translating a finished Chinese draft.

The series should become more abstract as it progresses, not more detailed about AMR implementation.
