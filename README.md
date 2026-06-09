# The Unofficial Guide — Project 1

---

## Domain

This RAG system makes student-generated casual information about FIU courses searchable and answerable. While official details regarding FIU courses and curriculum are readily available online, student-driven reviews on workload, difficulty, exam format, and content quality remain difficult to access. This project aims to bridge that gap, providing students with the insights needed to make informed decisions about course selection, majors, and career paths.

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
| 9 | StudentsReview - FIU | Alumni and student reviews of FIU programs and specific courses | http://www.studentsreview.com/professors/FL/Florida_International_University/ |
| 10 | Professors.directory - FIU | Aggregated course-level reviews and ratings for FIU | https://www.professors.directory/school/fl-florida_international_university/ |

**Note:** Sources actually collected and used in the pipeline: Reddit r/FIU (manual collection), PantherNOW (auto-scraped), and Professors Directory (auto-scraped). Other sources were blocked by JavaScript rendering, login walls, or bot protection and could not be scraped automatically.

---

## Chunking Strategy

**Chunk size:** ~250 tokens

**Overlap:** ~50 tokens

**Why these choices fit your documents:** The documents in this project are primarily short student reviews (1–5 sentences) with some longer multi-paragraph articles mixed in. A chunk size of ~250 tokens is large enough to fully contain the majority of reviews, ensuring key information is not split across chunks. The 50-token overlap preserves context at boundaries without significant duplication. Sentence-boundary splitting keeps individual opinions cohesive and avoids cutting mid-thought.

**Final chunk count:** 54 chunks across 3 documents
(panthernow.txt: 26, professorsdirectory.txt: 6, reddit_fiu.txt: 22)

**Sample chunks:**

**Chunk 1 — panthernow.txt**
"With housing being borderline impossible and little to no parking, it's clear why online course enrollment has increased. Aside from the impact of COVID and students getting comfortable with fully online-type courses, attending FIU can be borderline unachievable for many students..."

**Chunk 2 — panthernow.txt**
"Students already feel exponential pressure to ensure they have enough to compete. The unprecedented challenges of job uncertainty, AI, internships, and experience gaps pile up; students feel pressure to compensate outside of just university..."

**Chunk 3 — reddit_fiu.txt**
"POST: I need advice for the classes I am taking this FALL 2026 semester. I am currently speedrunning my civil engineering degree... This past semester was my best semester I've ever had in the last 19 years of my life, this is also the semester where I have taken the most classes and the hardest classes I've ever seen..."

**Chunk 4 — reddit_fiu.txt**
"COP 3337 - Kiavash is a good professor. He curves exams and even gives you extra credit at the end of the semester for completing the SPOT survey. The thing with Programming II is that you'll cover object oriented programming, from classes to OOP principles..."

**Chunk 5 — professorsdirectory.txt**
"Dr. Lopez is great. Like he said himself, he is clear when it comes to his grading. I took his Epigenetics course and it was very interesting. Our quizzes were a bit difficult but his tests were not so bad. I will recommend him for any class he teaches..."

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
For a production deployment serving thousands of FIU students, several tradeoffs would need to be considered. OpenAI's text-embedding-ada-002 would provide higher quality embeddings at low cost but introduces API dependency, latency, and per-request fees. Multilingual models like paraphrase-multilingual-MiniLM would better serve FIU's diverse Spanish-speaking student population who may write reviews in Spanish. Longer-context models could handle embedding multi-paragraph reviews without splitting them, improving retrieval quality for detailed posts. For this prototype, all-MiniLM-L6-v2 was chosen because it runs locally with no API key, has no rate limits, and performs well on short review-style text.

---

## Grounded Generation

**System prompt grounding instruction:**
The system prompt explicitly instructs the LLM to answer only from the retrieved documents:

```
You are a helpful assistant for FIU (Florida International University) students.
Answer questions using ONLY the information provided in the documents below.
Do NOT use any outside knowledge or make assumptions beyond what is stated.
Even if the documents only partially answer the question, provide the best answer
you can from the available information.
Only say "I don't have enough information on that in my current documents." if the
documents contain absolutely no relevant information.
Always cite which document(s) your answer came from at the end of your response.
```

**How source attribution is surfaced in the response:**
Source attribution is enforced in two ways. First, the system prompt instructs the LLM to cite which document(s) its answer came from. Second, the pipeline programmatically collects source filenames from ChromaDB metadata for every retrieved chunk and displays them in a separate "Retrieved From" panel in the Gradio UI, independent of what the LLM generates. This ensures source attribution is always visible even if the LLM forgets to mention it.

---

## Retrieval Test Results

**Query 1: "Is COP 4710 (Database Management) a difficult course?"**
Top chunks returned from reddit_fiu.txt (distance: 0.81). The retrieved chunks mentioned Database Management as a backup class option and discussed CS course difficulty generally. These are partially relevant — they confirm the course exists and is part of CS curriculum but do not directly discuss its difficulty.

**Query 3: "What do students say about online courses at FIU?"**
Top chunks returned from panthernow.txt (distance: 0.52). The retrieved chunks were highly relevant — multiple articles directly discussing FIU online course experiences, costs, and student opinions. This is the strongest retrieval result in the evaluation.

**Query 4: "What are the hardest CS courses at FIU according to students?"**
Top chunks returned from reddit_fiu.txt (distance: 0.80). The retrieved chunks were relevant — students directly naming Programming 3, Operating Systems, Data Structures, and Theory of Algorithms as hard courses. Good semantic match between the query and chunk content.

**Query 5: "How much programming experience is needed before taking COP 3530?"**
Top chunks returned from reddit_fiu.txt (distance: 0.84). Retrieved chunks discussed COP 2210 and COP 3337 as prerequisite courses and mentioned OOP experience as important. Partially relevant — the information is inferrable from the chunks even though the exact prerequisite requirement is not stated.

---

## Example Responses

**Example 1 — Strong grounded response (Query 3):**
> "According to the documents, students have mixed opinions about online courses at FIU. Some students appreciate the flexibility and accessibility that online courses provide, allowing them to customize their schedules to fit their individual needs and study from the comfort of their own homes (Document 1, Document 2). However, other students express concerns about the additional costs associated with online courses, with some feeling that they are being charged more than in-person students without utilizing the university's infrastructure (Document 3).
> Sources: Document 1 - panthernow.txt, Document 2 - panthernow.txt, Document 3 - panthernow.txt, Document 5 - panthernow.txt"

**Example 2 — Grounded response with partial information (Query 4):**
> "According to students, the hardest CS courses at FIU include: 1. Programming 3 and Operating Systems (Document 1 - reddit_fiu.txt), 2. Data Structures/Algorithms (Document 1 - reddit_fiu.txt), 3. Discrete Mathematics (Document 1 - reddit_fiu.txt), 4. Theory of Algorithms (Document 3 - reddit_fiu.txt).
> (Document 1 - reddit_fiu.txt, Document 3 - reddit_fiu.txt)"

**Example 3 — Out-of-scope query refusal:**
Query: "What is the GPA requirement for FIU honors program?"
> "I don't have enough information on that in my current documents."
This demonstrates proper grounding — the system correctly refuses to answer rather than generating a plausible-sounding but unsupported answer.

---

## Query Interface

The query interface is built with Gradio and runs locally at http://localhost:7860.

**Input fields:**
- "Select Question" dropdown — pre-loaded with the 5 evaluation plan questions for easy testing
- "Your Question" text box — accepts any free-text question the user types

**Output fields:**
- "Answer" — the LLM-generated response grounded in retrieved chunks, with inline document citations
- "Retrieved From" — lists the source filenames of the chunks used to generate the answer

**Sample interaction transcript:**

User selects: "What are the hardest CS courses at FIU according to students?"

System response:
"According to students, the hardest CS courses at FIU include: 1. Programming 3 and Operating Systems, 2. Data Structures/Algorithms, 3. Discrete Mathematics, 4. Theory of Algorithms. These courses are mentioned as particularly tough or requiring extra attention and effort. (Document 1 - reddit_fiu.txt, Document 3 - reddit_fiu.txt)"

Retrieved from: reddit_fiu.txt, panthernow.txt

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is COP 4710 (Database Management) a difficult course? | Reviews consistently mention high workload, challenging projects, requires significant time commitment | No direct information found. System noted COP 4710 was mentioned as a backup class option but could not determine difficulty. | Off-target | Inaccurate |
| 2 | What do students say about the exams in CHM 1045 (General Chemistry I)? | Exams are very difficult, cover a lot of material, require deep understanding beyond just memorizing | One student received 49% on the final exam. Lab component requires a report book. No detailed exam format information found. | Partially relevant | Partially accurate |
| 3 | What do students say about online courses at FIU? | Students mention flexibility, convenience, saves commute time but online fees are higher than in-person | Mixed opinions — flexibility and accessibility valued, but concerns about higher costs than in-person. FIU should equalize tuition rates. | Relevant | Accurate |
| 4 | What are the hardest CS courses at FIU according to students? | Programming 3, Operating Systems, and Data Structures are consistently mentioned as the hardest | Programming 3, Operating Systems, Data Structures, Discrete Math, and Theory of Algorithms named as hardest courses. | Relevant | Accurate |
| 5 | How much programming experience is needed before taking COP 3530 (Data Structures)? | Most advise taking Intro to Programming (COP 2210) and OOP (COP 3337) first to be well-prepared | Solid programming foundation needed. COP 2210 recommended before COP 3337. OOP experience important. Exact requirements not specified. | Partially relevant | Partially accurate |

---

## Failure Case Analysis

**Question that failed:** "Is COP 4710 (Database Management) a difficult course?"

**What the system returned:** "There is no information in the provided documents about the difficulty of COP 4710. However, it is mentioned that the poster is considering taking Database Management with another professor as a backup class. Since there is no direct information about COP 4710, the best answer is that there is not enough information to determine the difficulty of the course."

**Root cause (tied to a specific pipeline stage):** The failure originates at the data collection stage. The documents collected — PantherNOW articles, Professors Directory biography pages, and general Reddit course advice threads — do not contain specific reviews of COP 4710. During retrieval, ChromaDB returned chunks with distance scores above 1.0 (well above the 0.6 relevance threshold), indicating weak semantic matches. The embedding model found only surface-level keyword overlap with "Database Management" appearing once as a mentioned backup class option, not as a reviewed course. With no relevant chunks in context, the LLM correctly declined to generate an answer rather than hallucinating.

**What you would change to fix it:** Collect COP 4710-specific reviews from Rate My Professors or Reddit threads dedicated to that course. Adding even 3-4 direct student reviews of COP 4710 would give the retrieval system enough signal to return relevant chunks with distance scores below 0.6.

---

## Spec Reflection

**One way the spec helped you during implementation:**
The planning.md chunking strategy section was the most valuable part of the spec during implementation. Having pre-decided on 250-token chunks with 50-token overlap and sentence-aware splitting meant that when writing chunk_documents.py, the implementation decisions were already made. This prevented scope creep — instead of experimenting with different chunk sizes mid-implementation, the spec provided a clear target to implement and verify against. The requirement to print 5 sample chunks and inspect them before moving on was particularly useful, catching HTML artifacts and biography text that would have polluted the vector store.

**One way your implementation diverged from the spec, and why:**
The spec planned for 10 source documents across 10 different platforms, but the actual implementation used only 3 sources (PantherNOW, Professors Directory, Reddit). Most of the planned sources — Rate My Professors, Niche, Facebook, Coursicle, Uloop, and Koofers — block automated scraping through JavaScript rendering, login requirements, or bot protection. Rather than spending project time fighting scraper defenses, the approach shifted to manually collecting Reddit posts and auto-scraping the two accessible sources. The milestone instructions explicitly noted this was expected: "Some sources are difficult to scrape due to JavaScript rendering or blocked requests — you may need to copy text manually."

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md, specifying 250-token chunks, 50-token overlap, and sentence-aware splitting, along with sample review text from panthernow.txt.
- *What it produced:* A chunk_documents.py script using spaCy for sentence splitting and tiktoken for token counting. It split on sentence boundaries and accumulated sentences until the chunk size was reached, then started a new chunk with the last 2 sentences as overlap.
- *What I changed or overrode:* The initial script used `spacy`'s full NLP pipeline which was slow and unnecessary for simple sentence splitting. I simplified it to use Python's built-in period-based sentence splitting instead, which was faster and sufficient for the short review-style text in the documents.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section from planning.md specifying all-MiniLM-L6-v2 and ChromaDB, plus the pipeline diagram showing the 5 stages. I asked it to implement embed_chunks.py and retrieve.py.
- *What it produced:* A working embed_chunks.py that loaded chunks, generated embeddings, and stored them in ChromaDB with source metadata. It also produced a retrieve.py that queried the vector store and printed top-5 results with distance scores.
- *What I changed or overrode:* The initial chunk parser in embed_chunks.py used `raw.split("---")` as the separator, but the actual separator in all_chunks.txt was `\n\n---\n\n`. This caused 0 chunks to be parsed and stored. I debugged this by printing the raw file content and corrected the separator, which fixed the empty vector store issue.