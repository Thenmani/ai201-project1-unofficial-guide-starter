# The Unofficial Guide — Project 1

---

## Domain

This RAG system makes student generated casual information about FIU courses searchable and answerable.
While official details regarding FIU courses and curriculum are readily available online, student-driven reviews on workload, difficulty, exam format and content quality remain difficult to access. This project aims to bridge that gap, providing students with the insights needed to make informed decisions about course selection, majors, and career paths.


---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors - FIU | Student reviews and ratings for FIU professors and courses | https://www.ratemyprofessors.com/campusRatings.jsp?sid=1322 |
| 2 | Reddit - r/FIU | FIU student subreddit with discussions on courses, professors, and academic life | https://www.reddit.com/r/FIU/ | 
| 3 | Niche - FIU | Student reviews on academics, professors, and campus life at FIU | https://www.niche.com/colleges/florida-international-university/reviews/ |
| 4 | Coursicle - FIU | Course and professor information with student reviews and grade distributions | https://www.coursicle.com/fiu/ |
| 5 | Facebook - FIU Book Trade & Advice | FIU student group for textbook exchange and course advice | https://www.facebook.com/groups/FIUBoardofTrade/ |
| 6 | PantherNOW - Opinion | Student newspaper opinion pieces on courses and academic experiences | https://panthernow.com/category/opinion/ |
| 7 | Uloop - FIU Professor Reviews | Student reviews and ratings for FIU professors | https://fiu.uloop.com/professors/ |
| 8 | Koofers - FIU | Professor ratings, course reviews, and study materials for FIU | https://www.koofers.com/florida-international-university-fiu/ |
| 9 | StudentsReview – FIU | Alumni and student reviews of FIU programs and specific courses | http://www.studentsreview.com/professors/FL/Florida_International_University/ |
| 10 | Professors.directory – FIU | Aggregated course-level reviews and ratings for FIU | https://www.professors.directory/school/fl-florida_international_university/ |

---

## Chunking Strategy

**Chunk size:** ~250 tokens 

**Overlap:** ~50 tokens

**Why these choices fit your documents:** The chunk size of ~250 tokens matches the average length of a single review, ensuring that most reviews are kept intact within a single chunk. The overlap of ~50 tokens provides some additional context at chunk boundaries to avoid splitting key information across chunks.

**Final chunk count:** 54 chunks across 3 documents
(panthernow.txt: 26, professorsdirectory.txt: 6, reddit_fiu.txt: 22)
---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
- OpenAI's text-embedding-ada-002 would provide higher quality embeddings at a low cost
- Multilingual models like paraphrase-multilingual-MiniLM would better serve FIU's diverse Spanish-speaking student body 
- Longer context models could handle embedding multi-paragraph reviews without splitting them
- Accuracy on academic and course-specific jargon is important to validate for a production system

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->


**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report


| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is COP 4710 (Database Management) a difficult course? | Reviews consistently mention high workload, challenging projects, requires significant time commitment | TBD | TBD | TBD |
| 2 | What do students say about the exams in CHM 1045 (General Chemistry I)? | Exams are very difficult, cover a lot of material, require deep understanding beyond just memorizing | TBD | TBD | TBD |
| 3 | What do students say about online courses at FIU? | Students mention flexibility, convenience, saves commute time but online fees are higher than in-person | TBD | TBD | TBD |
| 4 | What are the hardest CS courses at FIU according to students? | Programming 3, Operating Systems, and Data Structures are consistently mentioned as the hardest | TBD | TBD | TBD |
| 5 | How much programming experience is needed before taking COP 3530 (Data Structures)? | Most advise taking Intro to Programming (COP 2210) and OOP (COP 3337) first to be well-prepared | TBD | TBD | TBD |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
