# -*- coding: utf-8 -*-
"""
The project forms: transferable shapes abstracted from the deployed Canvas work.

Each form is a SHAPE, not a copy. "Atomic Model Evolution Gallery" is useless to
a seventh-grade science teacher as a thing to reuse; the shape behind it -- build
a spatial gallery showing how an idea changed over time, you supply the idea and
the stages -- travels anywhere. So every form carries fields a teacher fills,
the same way the pedagogical moves in planner.html do, and names the real
instruments it was abstracted from so nothing here is invented.

`from_` entries are matched against the harvest by substring, and the builder
FAILS if a pattern matches nothing -- a form with no provenance is a form I made
up, and it should not ship.

Field types: text, num, area, sel (one of opts), mx (any of opts).
Tier is Optima's teacher-time tier: 3 = read closely against a rubric.
"""

FORMS = [

# ---------------------------------------------------------------- discussion
 {"id":"all-class-forum","kind":"discussion","name":"All-class forum on one scene",
  "makes":"A post on a single hard moment in the text, plus replies to two classmates.",
  "move":"Judge a particular act, with the text in front of you, where the answer is genuinely contested.",
  "why":"The whole cohort argues one question rather than each student answering a prompt alone. Replies stay hidden until a student posts, so nobody writes to the consensus.",
  "tier":2,"student_min":40,
  "fields":[
   {"k":"scene","l":"The scene, told plainly","t":"area","ph":"where we are, in three or four sentences, with the chapter"},
   {"k":"question","l":"The question","t":"area","ph":"answerable either way by someone who read carefully"},
   {"k":"strong","l":"What the strongest post does","t":"text","ph":"names the act, not the character"},
   {"k":"replies","l":"Replies required","t":"num","ph":"2"}],
  "from_":["All-Class Forum"]},

 {"id":"author-disagreement","kind":"project","name":"Letter of disagreement to the author",
  "makes":"A letter to a living or dead author saying, with reasons, where they are wrong.",
  "move":"State the other side at its strongest and fairest first, then answer it.",
  "why":"Turns 'respond to the text' into a real address to a real person. The two-step order is the whole exercise: no disagreeing until the claim has been put fairly.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"text","l":"The text and its claim","t":"area","ph":"what the author actually argues about how to live"},
   {"k":"fairest","l":"The claim at its strongest","t":"text","ph":"what the student must state before disagreeing"},
   {"k":"length","l":"Length","t":"text","ph":"a letter, not an essay"},
   {"k":"evidence","l":"Evidence required from the text","t":"text","ph":"how many places, and how cited"}],
  "from_":["Dear Author, I Disagree"]},

# ---------------------------------------------------------------- recordings
 {"id":"recorded-production","kind":"recording","name":"Recorded production with a run sheet",
  "makes":"A short recording in a named genre, built to a numbered run sheet.",
  "move":"Read a passage aloud as written, then do something with it in the voice the genre demands.",
  "why":"A run sheet with timings turns 'record a response' into a production. The genre carries the intellectual work: a critic judges, a commentator explains, a performer interprets.",
  "tier":3,"student_min":75,
  "fields":[
   {"k":"genre","l":"Genre","t":"sel","opts":["Broadcast review - read it, then judge it","Commentary track - read it, then go back over it","Audio drama - perform the scene, then explain one choice","Field record - read the account, then supply what it leaves out","Docent tour","Radio feature"]},
   {"k":"passage","l":"The passage read aloud","t":"area","ph":"named exactly, with chapter"},
   {"k":"segments","l":"The run sheet","t":"area","ph":"01 set-up :20-:30 / 02 the passage / 03 ... one line per segment, with timings"},
   {"k":"length","l":"Total length","t":"text","ph":"3 to 5 min"}],
  "from_":["Recorded Reading & Reflection","Voyage Documentary"]},

 {"id":"performance-recording","kind":"recording","name":"Perform it, then explain one choice",
  "makes":"A recording of the student performing, with a spoken or written note on one decision made.",
  "move":"Do the thing, then account for one deliberate choice inside it.",
  "why":"Cheap to set, hard to fake, and the explanation is where the learning shows. Works for music, recitation, a proof read aloud, a language passage.",
  "tier":3,"student_min":35,
  "fields":[
   {"k":"what","l":"What is performed","t":"text","ph":"the piece, scale, passage or pattern"},
   {"k":"how","l":"Acceptable means","t":"text","ph":"voice, keyboard, clapping, whatever they have"},
   {"k":"choice","l":"The choice they must explain","t":"text","ph":"the dynamic, the tempo, the emphasis"},
   {"k":"length","l":"Length","t":"text","ph":"short"}],
  "from_":["Perform a Rhythm","Ode to Joy Performance","Harmony Recording","C-Major Sing or Play"],
  "from_desc":["Performance Recording"]},

# ------------------------------------------------------------------- writing
 {"id":"synthesis-essay","kind":"project","name":"Synthesis essay on the module's own question",
  "makes":"A formal essay answering the question the whole module has been circling.",
  "move":"Take a position of your own and support it from several texts at once.",
  "why":"The module has a central question or it does not. If it does, this is the piece that proves the student can answer it rather than recite the readings.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"question","l":"The central question","t":"area","ph":"the one the module keeps returning to"},
   {"k":"texts","l":"Texts that must be drawn on","t":"area","ph":"named; how many must appear"},
   {"k":"length","l":"Length","t":"text","ph":"900 to 1,200 words"},
   {"k":"position","l":"What counts as a position","t":"text","ph":"as opposed to a summary of the readings"}],
  "from_":["How Ought a Person to Live?","Final Essay"]},

 {"id":"comparison-essay","kind":"project","name":"Comparison that answers a question",
  "makes":"An essay comparing two figures, works or cases to answer one essential question.",
  "move":"Use the comparison to settle something, not to list similarities and differences.",
  "why":"A comparison with no question behind it produces a Venn diagram in prose. Naming the question first is what makes it an argument.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"question","l":"The question the comparison answers","t":"area","ph":"e.g. what makes a good knight"},
   {"k":"pair","l":"What is compared, and who chooses","t":"text","ph":"two of a named set, student's choice"},
   {"k":"length","l":"Length","t":"text","ph":"5 to 6 paragraphs"},
   {"k":"builtfrom","l":"Earlier work this is built on","t":"text","ph":"the chart, the claim, the evidence log"}],
  "from_":["What Makes a Good Knight","Comparison"]},

 {"id":"cer-argument","kind":"project","name":"Claim, evidence, reasoning",
  "makes":"A short structured argument settling a question that has a determinable answer.",
  "move":"Commit to a claim, cite the evidence that bears on it, and show the reasoning that links them.",
  "why":"For questions where the student can be right or wrong and the interesting part is the warrant. The reasoning step is the one that gets skipped, so grade it hardest.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"question","l":"The question","t":"area","ph":"polar or nonpolar; which limits the reaction"},
   {"k":"evidence","l":"Evidence available to them","t":"area","ph":"the data, structure or text they must reason from"},
   {"k":"reasoning","l":"What the reasoning must connect","t":"text","ph":"the principle that makes the evidence count"},
   {"k":"length","l":"Length","t":"text","ph":"short and tight"}],
  "from_":["CER","Claim Evidence Reasoning"]},

 {"id":"indirect-evidence","kind":"project","name":"Argue for what cannot be seen",
  "makes":"An argument for something nobody has ever observed directly.",
  "move":"Build a case from what experiments reveal rather than from what anyone saw.",
  "why":"One of the few assignments that teaches what scientific knowledge actually is. Transfers anywhere the object is inferred: the atom, the interior of the earth, a lost manuscript, a prehistoric society.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"object","l":"The unseeable thing","t":"text","ph":"the atom; the mantle; the original text"},
   {"k":"history","l":"The succession of models","t":"area","ph":"who proposed what, and what forced each change"},
   {"k":"claim","l":"What the student must argue","t":"text","ph":"not what the model is, but why we believe it"},
   {"k":"length","l":"Length","t":"text","ph":""}],
  "from_":["How the Atom Cha"]},

 {"id":"op-ed-in-voice","kind":"project","name":"Op-ed in a borrowed voice",
  "makes":"An opinion piece addressed to a real public, written in a named historical voice.",
  "move":"Take on someone else's rhetoric and use it on a question of your own.",
  "why":"The persona forces attention to diction and audience in a way 'write an essay' never does. Requires verified quotations and citations, which is half the value.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"voice","l":"Whose voice","t":"text","ph":"Publius; a named pamphleteer"},
   {"k":"public","l":"Addressed to whom","t":"text","ph":"the citizenry; the assembly; a named readership"},
   {"k":"question","l":"The question at issue","t":"area","ph":""},
   {"k":"apparatus","l":"Citation required","t":"text","ph":"quotes verified, sources checked, MLA"}],
  "from_":["Publius Returns"]},

 {"id":"feeder-chain","kind":"project","name":"Feeder chain to one deep piece",
  "makes":"Four or five small graded steps across the module, ending in the one piece the teacher reads closely.",
  "move":"Build the argument in public, in stages, so nothing is written the night before.",
  "why":"The single most reusable project structure in the corpus. Each feeder is cheap to grade; only the last step costs real teacher time, and by then the student cannot fail for lack of a plan.",
  "tier":3,"student_min":300,
  "fields":[
   {"k":"final","l":"The final piece","t":"text","ph":"what the whole chain is for"},
   {"k":"steps","l":"The feeder steps, in order","t":"area","ph":"1 position / 2 evidence log / 3 thesis / 4 outline / 5 draft and final"},
   {"k":"weights","l":"Points on each step","t":"text","ph":"feeders light, final heavy"},
   {"k":"week","l":"Where each step falls","t":"text","ph":"one per week, final in the project week"}],
  "from_":["Project Feeder","Module Project"]},

 {"id":"choose-your-format","kind":"project","name":"One argument, the student picks the format",
  "makes":"The same argument delivered in a format the student chose weeks earlier and built toward.",
  "move":"Decide what form your case is best made in, then meet that form's standards.",
  "why":"Choice of format, committed to early and built weekly, gets far more out of students than choice of topic. The menu has to be real formats with real standards, not a worksheet with a costume.",
  "tier":3,"student_min":300,
  "fields":[
   {"k":"question","l":"The argument they all make","t":"area","ph":"the same question, whatever the format"},
   {"k":"menu","l":"The format menu","t":"area","ph":"essay / disputatio / journal / VR experience / short film / podcast or oration"},
   {"k":"chosen","l":"When the choice is locked","t":"text","ph":"week 3, and it does not change"},
   {"k":"standard","l":"How formats are held to one standard","t":"text","ph":"the rubric criteria that apply to all of them"}],
  "from_":["Make Your Argument"]},

 {"id":"lab-report","kind":"project","name":"Lab report from a measurement they made",
  "makes":"A report on a quantity the student actually measured, with the error accounted for.",
  "move":"Measure, compute, and then say honestly how far off you were and why.",
  "why":"The percent-error discussion is the part that teaches. A lab report of a result copied from a table teaches nothing.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"quantity","l":"What is measured","t":"text","ph":"density of an unknown; percent yield"},
   {"k":"method","l":"Method available at home","t":"area","ph":"what they can actually do with what they have"},
   {"k":"accepted","l":"The accepted value, and where it comes from","t":"text","ph":""},
   {"k":"error","l":"What the error discussion must address","t":"text","ph":"named sources, not 'human error'"}],
  "from_":["Lab Report"]},

 {"id":"structured-topic-analysis","kind":"project","name":"Diagram, then analysis, then a warranted claim",
  "makes":"A labelled diagram of a mechanism, a structured written analysis, and a short claim-evidence-reasoning section.",
  "move":"Draw the thing accurately, explain how it works, then argue one thing about it.",
  "why":"The workhorse of the corpus: thirty-two of these carry a whole science course. Pairs to one reading and one lesson, so the load is predictable, and the diagram catches misunderstanding that prose hides.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"topic","l":"The mechanism or structure","t":"text","ph":"protein folding; the membrane; the Krebs cycle"},
   {"k":"diagram","l":"What the diagram must be labelled with","t":"area","ph":"the parts, and what each interaction is"},
   {"k":"analysis","l":"What the analysis must explain","t":"area","ph":""},
   {"k":"claim","l":"The claim at the end","t":"text","ph":"one thing they must argue from it"},
   {"k":"paired","l":"Paired with","t":"text","ph":"the reading and lesson this follows"}],
  "from_":["Mapping the Four Levels","Krebs Cycle","The Membrane as a Governed"],
  "from_desc":["labeled diagram","Paired with"]},

 {"id":"paradigm-shift","kind":"project","name":"Trace how a model was replaced",
  "makes":"An analysis of one case where an accepted explanation gave way to a better one.",
  "move":"Follow the anomalies as they accumulate, then show what replaced the model and why.",
  "why":"Teaches that knowledge is revised rather than accumulated. The student picks the case from a short list, so the reading load stays real.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"options","l":"The cases they may choose from","t":"area","ph":"three, each with enough evidence to trace"},
   {"k":"pattern","l":"The pattern they must show","t":"text","ph":"anomaly accumulation, then model replacement"},
   {"k":"question","l":"The focus question","t":"area","ph":"what does the pattern of change tell us about the field"},
   {"k":"length","l":"Length","t":"text","ph":"400 to 600 words"}],
  "from_":["Paradigm Shift Analysis"]},

 {"id":"peer-review","kind":"project","name":"Review a supplied study",
  "makes":"A written peer review of a study the teacher provides, and a reflection on what made it weak or strong.",
  "move":"Judge someone else's work by stated standards, then say what would make you trust it.",
  "why":"A fictional study can be built to contain exactly the flaws you want found. Far more teachable than asking students to critique real published work they cannot evaluate.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"study","l":"The study they review","t":"area","ph":"written by you, with the flaws you want caught"},
   {"k":"criteria","l":"What they must judge it against","t":"area","ph":"sample, control, replication, claim size"},
   {"k":"reflection","l":"The reflection question","t":"text","ph":"what would make you want it replicated first"},
   {"k":"length","l":"Length","t":"text","ph":""}],
  "from_":["Peer Review in Practice"]},

 {"id":"thinker-profile","kind":"project","name":"Intellectual portrait, not a biography",
  "makes":"A profile of one thinker explaining the problem they were solving and the concepts they built to solve it.",
  "move":"Explain why someone's ideas were needed, not when they were born.",
  "why":"The instruction 'this is not a biography' does most of the work. Transfers to scientists, composers, mathematicians, founders.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"options","l":"Who they may choose","t":"area","ph":"a named list from the course"},
   {"k":"problem","l":"The question the profile must answer","t":"area","ph":"what problem was this person trying to solve"},
   {"k":"concepts","l":"How many concepts must be explained","t":"num","ph":"2"},
   {"k":"nowmatters","l":"Why it still matters","t":"text","ph":"the part students skip"}],
  "from_":["Classical Thinker Profile","Pop Artist Essay"],
  "from_desc":["appreciation essay"]},

 {"id":"case-study-series","kind":"project","name":"One concept per case, several times over",
  "makes":"A set of short reports, each applying one thinker's single concept to one real case.",
  "move":"Use a concept as a tool on something it was not written about.",
  "why":"Repetition with variation. Four short reports teach application better than one long essay, and each is small enough to be genuinely revised.",
  "tier":3,"student_min":360,
  "fields":[
   {"k":"concepts","l":"The concepts, one per report","t":"area","ph":"one per thinker or principle"},
   {"k":"cases","l":"Cases they may apply them to","t":"area","ph":"suggested, with room to propose their own"},
   {"k":"count","l":"How many reports","t":"num","ph":"4"},
   {"k":"length","l":"Length of each","t":"text","ph":"short"}],
  "from_":["Sociologist Case Study Reports"]},

 {"id":"field-observation","kind":"project","name":"Go and observe something real",
  "makes":"An observation report on a real setting the student visited, analysed with the course's frameworks.",
  "move":"Gather your own primary evidence, then interpret only what you actually saw.",
  "why":"The rule that evidence must be first-hand is what makes this work. Applicable far beyond social science: a building, an ecosystem, a rehearsal, a public meeting.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"settings","l":"Settings that qualify","t":"area","ph":"a list broad enough that everyone can reach one"},
   {"k":"frameworks","l":"Frameworks they analyse with","t":"area","ph":"named, from the course"},
   {"k":"rule","l":"The evidence rule","t":"text","ph":"what you saw, not what you read about places like it"},
   {"k":"length","l":"Length","t":"text","ph":""}],
  "from_":["Community Institution Study"]},

 {"id":"deep-after-survey","kind":"project","name":"Go deep on one after surveying many",
  "makes":"A researched profile of one instance, chosen from the many the course covered quickly.",
  "move":"After a wide fast survey, slow down and work one case the way a specialist would.",
  "why":"Answers the real problem with survey courses. The student chooses, so the depth is theirs, and the survey becomes the menu rather than the point.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"menu","l":"What they may choose from","t":"area","ph":"the traditions, periods or cases surveyed"},
   {"k":"depth","l":"What going deep requires","t":"area","ph":"sources, listening, terms used correctly"},
   {"k":"asspecialist","l":"The specialist whose method they borrow","t":"text","ph":"an ethnomusicologist; a palaeographer"},
   {"k":"length","l":"Length","t":"text","ph":""}],
  "from_":["World Music Research Profile"]},

 {"id":"capstone-proposal","kind":"project","name":"Evaluate something real, then propose",
  "makes":"A capstone that picks a real case, evaluates it with the course's frameworks, and recommends concrete changes.",
  "move":"Move from judgement to proposal, and make the proposal specific enough to act on.",
  "why":"Ends a course by pointing outward. The requirement that recommendations be concrete is the part that stops it becoming an essay about values.",
  "tier":3,"student_min":420,
  "fields":[
   {"k":"case","l":"What they may choose","t":"area","ph":"a community, an institution, a system, a site"},
   {"k":"frameworks","l":"Frameworks for the evaluation","t":"area","ph":""},
   {"k":"proposal","l":"What makes a recommendation concrete","t":"text","ph":"who does what, and how you would know it worked"},
   {"k":"length","l":"Length","t":"text","ph":""}],
  "from_":["Community Flourishing Capstone"]},

# -------------------------------------------------------------- making/studio
 {"id":"artwork-statement","kind":"project","name":"One finished piece, plus an artist statement",
  "makes":"A single finished artwork putting one named element or principle to work, with a short statement.",
  "move":"Make something real with a named technical constraint, then say what you were doing.",
  "why":"Forty of these carry three art courses. The constraint is what makes it teachable and gradable; the statement is what makes it thinking rather than craft alone.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"subject","l":"What they make","t":"text","ph":"the pot, the print, the cartouche, the mask"},
   {"k":"element","l":"The element or principle put to work","t":"text","ph":"value; pattern; one-point perspective"},
   {"k":"materials","l":"Materials, with a home alternative","t":"area","ph":"clay or salt dough; paper plate or cardboard"},
   {"k":"statement","l":"What the statement must say","t":"text","ph":"the choice made, and why"}],
  "from_":["Artist Statement"],
  "from_desc":["WEEK 2 ARTWORK","Studio project","YOUR PROJECT"]},

 {"id":"themed-series","kind":"project","name":"A series unified by one theme",
  "makes":"Three or more original pieces held together by a single theme, meeting a checklist of techniques.",
  "move":"Sustain one idea across several pieces instead of one piece at a time.",
  "why":"A series exposes whether a student has an idea or only a technique. The technical checklist keeps it assessable without dictating the theme.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"count","l":"How many pieces","t":"num","ph":"3"},
   {"k":"theme","l":"What may serve as the unifying theme","t":"area","ph":"subject, a technique, movement, texture, colour"},
   {"k":"checklist","l":"Techniques that must appear","t":"area","ph":"at least two lighting techniques; one showing texture"},
   {"k":"reflection","l":"The reflection","t":"text","ph":"what holds the series together"}],
  "from_":["Edited Photo Series"]},

 {"id":"best-work","kind":"project","name":"Choose your strongest work and defend it",
  "makes":"Two or three of the student's own earlier pieces, selected, with a reflection justifying the choice.",
  "move":"Judge your own work against a standard and say why these are the best of it.",
  "why":"Costs nothing to produce and teaches self-assessment better than any rubric. Resubmitting existing files is the point, not a loophole.",
  "tier":2,"student_min":45,
  "fields":[
   {"k":"window","l":"Which earlier work is eligible","t":"text","ph":"weeks 5 to 7"},
   {"k":"count","l":"How many they choose","t":"num","ph":"3"},
   {"k":"criteria","l":"What they must name about each","t":"area","ph":"the technique used on purpose; why it is their strongest"},
   {"k":"redo","l":"The one thing they would do differently","t":"text","ph":""}],
  "from_":["My Strongest Work"]},

 {"id":"two-intentions","kind":"project","name":"Same subject, two opposite intentions",
  "makes":"Two versions of the same subject, each made with a deliberately opposite aim, plus a comparison.",
  "move":"Change one decision and watch the meaning change.",
  "why":"The cleanest way to teach that choices are choices. Transfers well past art: two openings to the same essay, two graphs of one dataset, two translations of one line.",
  "tier":3,"student_min":75,
  "fields":[
   {"k":"subject","l":"The subject, held constant","t":"text","ph":"one subject, shot or made twice"},
   {"k":"a","l":"Intention A","t":"text","ph":"include the context"},
   {"k":"b","l":"Intention B","t":"text","ph":"exclude everything but the subject"},
   {"k":"compare","l":"What the comparison must explain","t":"text","ph":"what was gained and what was lost"}],
  "from_":["An Intentional Photograph"]},

 {"id":"combine-two","kind":"project","name":"Combine two things into one new thing",
  "makes":"One recognisable new form built by combining and editing at least two simple parts.",
  "move":"Make the join disappear, so the result reads as one thing and not two side by side.",
  "why":"Deceptively hard and immediately assessable: either it reads as one form or it does not. Works for shapes, motifs, melodies, sentences, arguments.",
  "tier":3,"student_min":75,
  "fields":[
   {"k":"parts","l":"The parts to combine","t":"text","ph":"at least two shapes, each starting separate"},
   {"k":"result","l":"What the result must be","t":"text","ph":"one recognisable object, symbol or character"},
   {"k":"evidence","l":"Evidence of the process","t":"text","ph":"layers kept; drafts shown"},
   {"k":"tool","l":"Tool or medium","t":"text","ph":""}],
  "from_":["Two Are Better Than One"]},

 {"id":"corrective","kind":"project","name":"Fix something deliberately broken",
  "makes":"A corrected version of a flawed artifact the teacher supplies, with a note on what was changed.",
  "move":"Diagnose the fault, repair it, and be able to say what you did.",
  "why":"Supplying the flawed original removes the 'I had nothing to work with' failure and lets you aim at exactly one skill. Cheap to set up, easy to grade.",
  "tier":2,"student_min":45,
  "fields":[
   {"k":"given","l":"The flawed original","t":"area","ph":"a badly exposed photo; a paragraph with a broken argument"},
   {"k":"tools","l":"Tools they must use","t":"area","ph":"at least two of the named adjustments"},
   {"k":"preserve","l":"What must be preserved","t":"text","ph":"work on a duplicate; keep the original intact"},
   {"k":"note","l":"What the note must say","t":"text","ph":""}],
  "from_":["Editing & Exposure","Color Editing & Filters"]},

 {"id":"ordinary-extraordinary","kind":"project","name":"Make the ordinary extraordinary",
  "makes":"One piece that treats a deliberately dull everyday object with real technique.",
  "move":"Find the interest in something with none, using specific named techniques.",
  "why":"Removes subject matter as a way to score points. Nobody can coast on an exciting topic, so the technique is all that is left.",
  "tier":3,"student_min":75,
  "fields":[
   {"k":"object","l":"How the object is chosen","t":"text","ph":"from a shot list you supply; ordinary is required"},
   {"k":"techniques","l":"Techniques that must appear","t":"area","ph":"one line type; a clear use of space; one framing choice"},
   {"k":"reflection","l":"The reflection questions","t":"area","ph":"what did you choose, and what made it interesting"},
   {"k":"medium","l":"Medium","t":"text","ph":""}],
  "from_":["Making the Ordinary Extraordinary"]},

 {"id":"master-copy-then-own","kind":"project","name":"Do what the master did, then do your own",
  "makes":"A piece made by the master's actual method, not merely in the master's style.",
  "move":"Reproduce the process, then use the process on something of your own.",
  "why":"The distinction between imitating a look and imitating a method is the whole of atelier teaching. Say which one you want.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"master","l":"The master and the work","t":"text","ph":"named, with the work in front of them"},
   {"k":"method","l":"The method being reproduced","t":"area","ph":"carved, not painted; ground first, then glazed"},
   {"k":"own","l":"What they make with it","t":"text","ph":"their own subject, the master's method"},
   {"k":"statement","l":"What the statement addresses","t":"text","ph":"where the method resisted them"}],
  "from_":["My Own Great Wave"]},

 {"id":"booklet","kind":"project","name":"A booklet, one page per item",
  "makes":"A folded booklet with a cover and one page for each item in a set.",
  "move":"Give every member of a set its own page, and make the pages sit together as one object.",
  "why":"Turns a review list into a made thing. The physical constraint of a folded sheet does the design work for you.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"set","l":"The set","t":"text","ph":"the seven elements; the parts of speech; the cell organelles"},
   {"k":"pages","l":"Pages, including the cover","t":"num","ph":"8"},
   {"k":"perpage","l":"What each page must carry","t":"area","ph":"the name, an example made by them, one sentence"},
   {"k":"format","l":"Format","t":"text","ph":"one folded sheet"}],
  "from_":["Review Booklet"]},

 {"id":"identity-artifact","kind":"project","name":"A piece that introduces you as a practitioner",
  "makes":"A cover or opening piece that says who the student is in this discipline.",
  "move":"Use the discipline's own tools to say something about yourself.",
  "why":"A good first assignment. Every technical requirement is met in service of something the student actually wants to say, and it becomes the front of their portfolio.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"canvas","l":"Format and size","t":"text","ph":"1920 x 1080; one page; 60 seconds"},
   {"k":"required","l":"Technical requirements","t":"area","ph":"a filled background; three deliberate shapes; your name and date"},
   {"k":"personal","l":"The element that says something about them","t":"text","ph":"a colour scheme, an initial, a symbol"},
   {"k":"restraint","l":"The restraint","t":"text","ph":"keep it simple and deliberate"}],
  "from_":["This Is Me as a Digital Artist"]},
]
