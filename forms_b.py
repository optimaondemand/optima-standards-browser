# -*- coding: utf-8 -*-
"""
Project forms, part two: world-building, VR, real-world work, and assessment.

Same schema as forms.py. Split across two modules only so each stays readable.
"""

FORMS_B = [

# --------------------------------------------- world-building / imagination
 {"id":"lost-scene","kind":"project","name":"Write the scene the author left out",
  "makes":"An original scene that belongs in an existing work but is not in it, plus a director's note.",
  "move":"Write inside someone else's world convincingly enough that the seam does not show.",
  "why":"Demands closer reading than an analysis essay, because a wrong detail is visible. The director's note is where the student argues the scene earns its place.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"work","l":"The work, and where the gap is","t":"area","ph":"the moment the text skips over"},
   {"k":"constraints","l":"What the scene must honour","t":"area","ph":"voice, verse form, what the characters already know"},
   {"k":"note","l":"What the director's note argues","t":"text","ph":"why this scene, staged this way"},
   {"k":"passes","l":"Revision passes required","t":"num","ph":"3"}],
  "from_":["Elsinore Stage"]},

 {"id":"first-contact-story","kind":"project","name":"Make a strange place feel real",
  "makes":"An original short story set somewhere the reader has never been.",
  "move":"Borrow an author's world-building method and use it on a world of your own.",
  "why":"The model is studied for a whole module first, so this is imitation with the pattern already absorbed rather than a blank invitation to be creative.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"model","l":"The author whose method they borrow","t":"text","ph":"and what specifically that method is"},
   {"k":"technique","l":"The technique, named","t":"area","ph":"give the reader one familiar thing to stand on, then change everything else"},
   {"k":"length","l":"Length","t":"text","ph":"2 to 3 pages"},
   {"k":"constraint","l":"The constraint","t":"text","ph":"first contact; one location; nothing explained to the reader"}],
  "from_":["Week 6 - Short Story"]},

 {"id":"character-monologue","kind":"project","name":"A new voice in a world you built",
  "makes":"An original monologue in the voice of a character the student invents, set in a world they built earlier.",
  "move":"Speak as someone who is not you, inside constraints you set yourself.",
  "why":"Pays off earlier world-building instead of abandoning it. Written then performed, so the prose has to survive being said aloud.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"world","l":"The world it belongs to","t":"text","ph":"the one they built across the module"},
   {"k":"who","l":"Who speaks, and what they want","t":"area","ph":""},
   {"k":"length","l":"Length","t":"text","ph":""},
   {"k":"performed","l":"How it is performed","t":"sel","opts":["Read aloud, recorded","Performed in the VR space","Live to the class","Not performed"]}],
  "from_":["Malacandra Speaks"]},

 {"id":"form-constrained-poem","kind":"project","name":"A fixed form that has to argue",
  "makes":"An original poem in a strict form that makes a case rather than describing a feeling.",
  "move":"Meet the form exactly, and make the form do the arguing.",
  "why":"Fourteen lines that argue is a far better assignment than write a sonnet. The turn in the form becomes the turn in the argument.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"form","l":"The form","t":"text","ph":"sonnet; villanelle; ghazal; syllabic"},
   {"k":"rules","l":"Rules that must be met exactly","t":"area","ph":"line count, metre, rhyme, where the turn falls"},
   {"k":"argue","l":"What it must argue","t":"area","ph":"a claim, not a mood"},
   {"k":"craft","l":"The craft statement","t":"text","ph":"where they broke a rule on purpose, and why"}],
  "from_":["Final Original Sonnet","Full Draft Sonnet"]},

 {"id":"imitate-pattern","kind":"project","name":"Write in a poet's structural pattern",
  "makes":"An original piece built on one poet's structural habit, then performed.",
  "move":"Take a pattern rather than a subject, and put your own material through it.",
  "why":"Naming the pattern gives students something to actually do. Far more productive than write a poem inspired by.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"poet","l":"The poet and the pattern","t":"text","ph":"a juxtaposition; a catalogue; anaphora"},
   {"k":"length","l":"Length","t":"text","ph":"6 to 12 lines"},
   {"k":"subject","l":"What they may write about","t":"text","ph":"their own material, not the poet's"},
   {"k":"performance","l":"Where it is performed","t":"text","ph":"under a VR night sky; to the class"}],
  "from_":["Juxtaposition Poem"]},

 {"id":"time-capsule","kind":"project","name":"Seal the work into a time capsule",
  "makes":"One document gathering what the student built across the module and what they came to understand, addressed to a future reader.",
  "move":"Explain your own work to someone who will meet it before they meet the source.",
  "why":"Gives built work, especially VR and studio work, a written home. The future-reader address gets better prose than a reflection prompt ever does.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"built","l":"What was built across the module","t":"area","ph":"the storyboard, the space, the series"},
   {"k":"reader","l":"Who the future reader is","t":"text","ph":"someone who will walk your village before reading the novel"},
   {"k":"parts","l":"What the capsule must contain","t":"area","ph":"images, the arc, what changed in their understanding"},
   {"k":"format","l":"Format","t":"text","ph":"one Word document"}],
  "from_":["Time Capsule"]},

 {"id":"cover-and-claim","kind":"project","name":"A cover, and what the cover claims",
  "makes":"A cover for a work the class read, plus a reflection defending what the cover asserts about it.",
  "move":"Compress a whole work into one image, then defend the compression.",
  "why":"Every design decision becomes an interpretive claim, which is what makes the reflection worth grading. Any medium is fine, so materials are never the barrier.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"work","l":"The work","t":"text","ph":""},
   {"k":"medium","l":"Medium","t":"text","ph":"student's choice, drawn or digital"},
   {"k":"required","l":"What must appear","t":"area","ph":"title, author, one central image"},
   {"k":"defence","l":"What the reflection defends","t":"area","ph":"what the cover claims the book is about, and why"}],
  "from_":["ACC Final Project"]},

 {"id":"mock-trial","kind":"project","name":"Advocate's brief and closing argument",
  "makes":"A formal brief arguing one side, plus a recorded closing argument.",
  "move":"Argue for a side you were assigned, to a standard of proof.",
  "why":"The brief and the spoken close test different things: one is structure, the other is persuasion under time. Works for any text with a judgement in it.",
  "tier":3,"student_min":300,
  "fields":[
   {"k":"charge","l":"What is at issue","t":"area","ph":"stated so both sides are genuinely arguable"},
   {"k":"side","l":"How sides are assigned","t":"text","ph":"assigned, not chosen"},
   {"k":"brief","l":"What the brief must contain","t":"area","ph":"the standard of proof; evidence from the text only"},
   {"k":"close","l":"The closing argument","t":"text","ph":"recorded, and how long"}],
  "from_":["Trial of Oedipus","Bard"]},

# --------------------------------------------------------------------- VR
 {"id":"vr-gallery","kind":"project","name":"Build a gallery, then guide someone through it",
  "makes":"A spatial gallery of stations the student builds, and a recorded walkthrough given as its docent.",
  "move":"Arrange knowledge in space so the order carries the argument, then narrate it live.",
  "why":"The strongest VR form in the corpus and the one that transfers furthest: how a model changed, how a tradition spread, how a character developed. Ships with a no-headset narrated alternative every time.",
  "tier":3,"student_min":180,
  "fields":[
   {"k":"stations","l":"The stations, and what each holds","t":"area","ph":"one per stage, tradition or thinker"},
   {"k":"order","l":"What the ordering has to argue","t":"text","ph":"the sequence is the claim"},
   {"k":"narration","l":"What the docent must say at each stop","t":"area","ph":""},
   {"k":"alternate","l":"The no-headset pathway","t":"text","ph":"a narrated walkthrough of the same stations"},
   {"k":"length","l":"Recording length","t":"text","ph":""}],
  "from_":["Evolution Gallery","Museum","Meet the Thinkers","Showcase"]},

 {"id":"vr-storyboard","kind":"project","name":"Build the story's arc in the space",
  "makes":"A multi-panel storyboard built in the space, carrying a narrative from start to end.",
  "move":"Choose the few moments that carry the whole arc, and place them where they can be walked.",
  "why":"Selecting six panels from a whole book is the analytical work; building them is the reward. Ends with something the student can show someone.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"story","l":"The story","t":"text","ph":""},
   {"k":"panels","l":"How many panels, and what each carries","t":"area","ph":"six, from first cause to final consequence"},
   {"k":"setting","l":"The setting they build","t":"text","ph":"student's choice of location"},
   {"k":"alternate","l":"The no-headset pathway","t":"text","ph":""}],
  "from_":["Creative + VR","Time Capsule"]},

 {"id":"vr-perform-own","kind":"project","name":"Perform your own work in the space",
  "makes":"A recording of the student performing something they wrote, in a space they chose.",
  "move":"Deliver your own composition somewhere that suits it, and say why it suits it.",
  "why":"Solo, unscheduled, and the choice of location is the student's, which is where the thought is. Cheap to run, and it makes writing into an occasion.",
  "tier":3,"student_min":60,
  "fields":[
   {"k":"work","l":"What they perform","t":"text","ph":"their poem, melody, monologue"},
   {"k":"location","l":"Location","t":"text","ph":"student's choice; they say why it suits the piece"},
   {"k":"describe","l":"What they describe afterwards","t":"text","ph":"in the vocabulary taught"},
   {"k":"alternate","l":"The no-headset pathway","t":"text","ph":""}],
  "from_":["VR Melody","VR Gallery Finale"]},

# --------------------------------------------------- real world and career
 {"id":"portfolio-artifact","kind":"project","name":"A real thing you could actually send",
  "makes":"A finished professional artifact built to real-world standards, not to a rubric.",
  "move":"Make something whose audience is not your teacher.",
  "why":"The framing does the work: not a worksheet for a grade, but the first piece of a portfolio carried out of the course. Resume, one-way video, cover letter, portfolio page.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"artifact","l":"The artifact","t":"text","ph":"a one-page resume; a recorded one-way interview"},
   {"k":"audience","l":"Its real audience","t":"text","ph":"who would actually receive it"},
   {"k":"standard","l":"The real-world standard it must meet","t":"area","ph":"length, format, what a recruiter looks for"},
   {"k":"reuse","l":"Where it is used later","t":"text","ph":"the portfolio it becomes part of"}],
  "from_":["Real Portfolio Artifact","One-Way Video"]},

 {"id":"options-comparison","kind":"project","name":"Real options, side by side, on your own criteria",
  "makes":"A researched comparison of real options against criteria the student defines first.",
  "move":"Decide what matters to you before you compare, then hold the options to it.",
  "why":"Defining the criteria first is the whole exercise, and it is the step students skip. Works for colleges, careers, methods, technologies, sources.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"options","l":"What is compared","t":"text","ph":"two careers; four paths; real named colleges"},
   {"k":"criteria","l":"Criteria they define first","t":"area","ph":"what fit means to them, written before the research"},
   {"k":"sources","l":"Sources that count","t":"area","ph":"BLS, O*NET, OECD, College Scorecard, apprenticeship.gov"},
   {"k":"verdict","l":"What they must conclude","t":"text","ph":"a ranked answer, not a table"}],
  "from_":["Path Comparison","Career & Major Exploration","College Shortlist"]},

 {"id":"draft-then-revise","kind":"project","name":"Draft it early, revise it at the end",
  "makes":"The same plan or position written twice: a first draft early, revised at the course's end.",
  "move":"Confront what you thought before you knew anything.",
  "why":"The best evidence of learning a course can produce, because the student sees it themselves. Costs one extra assignment slot and pays for itself.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"artifact","l":"What gets drafted and revised","t":"text","ph":"a 1-year and 5-year plan; a position on the central question"},
   {"k":"when","l":"When each version is due","t":"text","ph":"draft in module 2, revision at the end"},
   {"k":"changed","l":"What they must account for","t":"area","ph":"what changed, and what made it change"},
   {"k":"keep","l":"What must be preserved from the draft","t":"text","ph":"so the comparison stays visible"}],
  "from_":["Finalize Your 1-Year and 5-Year Plan"]},

 {"id":"pitch-deck","kind":"project","name":"Six slides that carry the whole case",
  "makes":"A short deck plus speaker notes, preceded by a brief naming the audience and the problem.",
  "move":"Cut a case down until every word earns its place, for a named room.",
  "why":"The slide limit is the teacher. Built in short weekly sittings, so it is a term-long project that never needs a crisis week.",
  "tier":3,"student_min":300,
  "fields":[
   {"k":"case","l":"What is being pitched","t":"area","ph":""},
   {"k":"audience","l":"Who is in the room","t":"text","ph":"researched, not imagined"},
   {"k":"slides","l":"Slide count","t":"num","ph":"6"},
   {"k":"cadence","l":"When it gets built","t":"text","ph":"one sitting a week, about 30 minutes"}],
  "from_":["Pitch Deck","Audience & Problem Brief"]},

 {"id":"ai-assisted-draft","kind":"project","name":"AI as a drafting partner, then your revision",
  "makes":"A first draft produced with an AI tool, then a revision the student owns, with the changes named.",
  "move":"Use the tool, then improve on it, and be able to say exactly where it was wrong.",
  "why":"Teaches the judgement rather than the tool. The graded object is the revision and the account of what changed, so nothing rewards accepting the output.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"task","l":"What the draft is of","t":"area","ph":""},
   {"k":"use","l":"What the tool is used for","t":"text","ph":"research and first drafting, not the final text"},
   {"k":"account","l":"What they must report","t":"area","ph":"what they kept, what they cut, and why it was wrong"},
   {"k":"note","l":"Note","t":"text","ph":"no AI tool is required; an unaided draft is a full-credit path"}],
  "from_":["AI-Assisted Planning"]},

# ------------------------------------------------------------- listening
 {"id":"listening-response","kind":"project","name":"Listen to several, describe what you hear",
  "makes":"A written response describing named qualities heard across several pieces.",
  "move":"Put a heard impression into the discipline's vocabulary.",
  "why":"Cheap, repeatable, and it forces the vocabulary into use. Covering several pieces stops one lucky description carrying the answer.",
  "tier":2,"student_min":40,
  "fields":[
   {"k":"pieces","l":"What they listen to","t":"area","ph":"three, named, and where to find them"},
   {"k":"vocabulary","l":"Terms that must be used","t":"area","ph":"dynamics, tempo, articulation"},
   {"k":"count","l":"How many must be described","t":"num","ph":"3"},
   {"k":"length","l":"Length","t":"text","ph":"a paragraph each"}],
  "from_":["Listening Essay"]},

 {"id":"perform-plus-fact","kind":"project","name":"A short performance and one researched fact",
  "makes":"A brief recorded performance paired with one thing the student found out.",
  "move":"Do it, and know something about whoever did it first.",
  "why":"Pairs skill with knowledge in one small assignment. The single-fact limit keeps it honest in the lower grades.",
  "tier":2,"student_min":30,
  "fields":[
   {"k":"perform","l":"What they perform","t":"text","ph":""},
   {"k":"fact","l":"What the fact must be about","t":"text","ph":"the composer, the tradition, the instrument"},
   {"k":"source","l":"Where the fact comes from","t":"text","ph":""},
   {"k":"length","l":"Length","t":"text","ph":"short"}],
  "from_":["Jazz Fact and Performance","Mozart and Quarter Notes"]},

# ------------------------------------------------------------ assessment
 {"id":"random-draw-exam","kind":"assessment","name":"Exam drawn from quizzes already taken",
  "makes":"A cumulative exam assembled at random from quiz items students have already met.",
  "move":"Recall across the whole course, with nothing new on the paper.",
  "why":"Every student sees a different paper, nothing on it is unseen, and it costs no teacher grading time. The fairest cumulative exam in the corpus.",
  "tier":1,"student_min":90,
  "fields":[
   {"k":"pool","l":"Which weeks the draw covers","t":"text","ph":"any week without its own quiz is excluded"},
   {"k":"perweek","l":"Items drawn per week","t":"num","ph":"3"},
   {"k":"value","l":"Points per item","t":"num","ph":"2"},
   {"k":"note","l":"What students are told","t":"text","ph":"nothing here is new; no two papers are the same"}],
  "from_":["Final Examination"]},

 {"id":"identification-exam","kind":"assessment","name":"Identify it from a described example",
  "makes":"An exam where each item describes a real example and the student names what it is.",
  "move":"Recognise the thing from its features rather than from its label.",
  "why":"Tests whether a survey actually took. Written as descriptions rather than embedded media, so it survives any platform and any bandwidth.",
  "tier":1,"student_min":45,
  "fields":[
   {"k":"domain","l":"What is identified","t":"text","ph":"the tradition, instrument, technique or element"},
   {"k":"partA","l":"Identification section","t":"text","ph":"10 items, 2 points each"},
   {"k":"partB","l":"Vocabulary and context section","t":"text","ph":"8 multiple choice plus 2 short answer"},
   {"k":"guide","l":"When the study guide is posted","t":"text","ph":"two modules ahead"}],
  "from_":["Q1 Exam","Q2 Exam"]},

 {"id":"notation-analysis-exam","kind":"assessment","name":"Write it, analyse it, identify it",
  "makes":"A three-part assessment: a construction or notation task, an analysis section, and identification.",
  "move":"Produce the notation yourself, not only recognise it.",
  "why":"The construction section separates knowing the rule from being able to use it. Applies to music theory, proofs, chemical equations, grammar diagrams.",
  "tier":3,"student_min":120,
  "fields":[
   {"k":"construct","l":"The construction task","t":"area","ph":"write and label the intervals and triads"},
   {"k":"analyse","l":"The analysis section","t":"area","ph":"short answer on a given example"},
   {"k":"identify","l":"The identification section","t":"text","ph":""},
   {"k":"weights","l":"Points across the parts","t":"text","ph":""}],
  "from_":["Fundamentals Assessment","Assessment - Counterpoint"]},

 {"id":"two-part-final","kind":"project","name":"Two-part final: the argument and the made thing",
  "makes":"A written argument and a creative or spatial piece on the same idea, graded together.",
  "move":"Say it in prose, then say it again in a form that cannot use prose.",
  "why":"Students who write well and students who make well each get somewhere to succeed, and both have to do the other. The halves must address the same idea or it is simply two assignments.",
  "tier":3,"student_min":240,
  "fields":[
   {"k":"idea","l":"The one idea both halves address","t":"area","ph":""},
   {"k":"written","l":"The written half","t":"text","ph":"length and kind"},
   {"k":"made","l":"The made half","t":"text","ph":"visual, VR scene, recording"},
   {"k":"reflection","l":"What ties them together","t":"text","ph":"the reflection that names the connection"}],
  "from_":["Final Project Written","Final Project Creative"]},

 {"id":"four-step-analysis","kind":"project","name":"Four-step analysis of one work",
  "makes":"A written analysis of a single work in four ordered steps: describe, analyse, interpret, judge.",
  "move":"Look before you interpret, and do not judge before you have described.",
  "why":"The order is the discipline. Students want to leap to what it means, and the describe step is where they are made to actually look. One paragraph per step makes skipping visible. Repeated on harder objects all year it becomes a habit rather than an assignment.",
  "tier":3,"student_min":90,
  "fields":[
   {"k":"work","l":"The work, with its date and maker","t":"area","ph":"and where they can see it"},
   {"k":"vocabulary","l":"Vocabulary they must use","t":"area","ph":"the terms from this unit, named"},
   {"k":"weighting","l":"Which step carries the most weight here","t":"text","ph":"with no written record, describe and analyse carry it"},
   {"k":"length","l":"Length","t":"text","ph":"one paragraph per step"}],
  "from_":["Analysis"],
  "from_desc":["four-part analysis","four-step analysis"]},

 {"id":"define-and-label","kind":"project","name":"Define it in your own words, then label it",
  "makes":"A short written response defining the terms in the student's own words, plus a labelling or notation task.",
  "move":"Say what it means without the book, then point to it correctly on the real thing.",
  "why":"The two halves catch different failures: a student can define a term they cannot recognise, and recognise one they cannot define. Small, quick, and it works in any subject with a vocabulary.",
  "tier":2,"student_min":30,
  "fields":[
   {"k":"terms","l":"The terms","t":"area","ph":"named, and how many"},
   {"k":"ownwords","l":"What counts as their own words","t":"text","ph":"complete sentences, not the glossary"},
   {"k":"label","l":"The labelling task","t":"area","ph":"name the notes on the staff; label the diagram"},
   {"k":"example","l":"Example required with each","t":"text","ph":"one real instance per term"}],
  "from_":["Parameters Overview","Tone and Notes","Reading Response"]},

 {"id":"personal-inventory","kind":"project","name":"An honest inventory of where you are now",
  "makes":"A document capturing the student's own goals, readiness and gaps at this moment.",
  "move":"Assess yourself accurately, including what is not going well.",
  "why":"The foundation piece for anything later built on self-knowledge: a resume, an essay, a plan. Honest is the operative word, and the assignment has to say so or it becomes an advertisement.",
  "tier":3,"student_min":75,
  "fields":[
   {"k":"sections","l":"What the inventory covers","t":"area","ph":"goals, honest readiness, what is missing"},
   {"k":"honesty","l":"How honesty is protected","t":"text","ph":"graded on specificity, never on how good it looks"},
   {"k":"usedlater","l":"What it feeds","t":"text","ph":"the resume, the essay, the shortlist"},
   {"k":"format","l":"Format","t":"text","ph":"one Word document"}],
  "from_":["Personal Stock Inventory"]},

 {"id":"influence-map","kind":"project","name":"Draw the influence, do not list it",
  "makes":"A visual map showing how several things a course covered influenced one another.",
  "move":"Show the connections as connections, so the shape of the story is visible at once.",
  "why":"A survey covers many things and students remember them as a list. Drawing the influence forces them to commit to what caused what, and the errors are visible in a way prose hides. Works for musical traditions, philosophical schools, scientific ideas, historical events, literary movements.",
  "tier":3,"student_min":150,
  "fields":[
   {"k":"items","l":"What goes on the map","t":"area","ph":"the traditions, schools or ideas from these modules"},
   {"k":"claim","l":"The story the map has to tell","t":"area","ph":"how they collided and what came out of it"},
   {"k":"edges","l":"What an arrow has to mean","t":"text","ph":"influence, with a reason, not proximity"},
   {"k":"medium","l":"Medium","t":"text","ph":"drawn, digital, or built in the space"}],
  "from_":["Cultural Roots Map"]},
]
