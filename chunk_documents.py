import os
import tiktoken

print("Current directory:", os.getcwd())
print("Files in data/:", os.listdir('data') if os.path.exists('data') else "data/ folder NOT FOUND")

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoding.encode(text))

def chunk_text(text, source, chunk_size=250, overlap=50):
    # Split into sentences by period
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 0]
    
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence = sentence + '.'
        sentence_tokens = count_tokens(sentence)

        if current_tokens + sentence_tokens <= chunk_size:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
        else:
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                if len(chunk_text.strip()) > 0:
                    chunks.append({
                        'text': chunk_text,
                        'source': source,
                        'tokens': current_tokens
                    })

            # Start new chunk with overlap
            overlap_chunk = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
            current_chunk = overlap_chunk + [sentence]
            current_tokens = sum(count_tokens(s) for s in current_chunk)

    # Add last chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        if len(chunk_text.strip()) > 0:
            chunks.append({
                'text': chunk_text,
                'source': source,
                'tokens': current_tokens
            })

    return chunks

# Process all files in data/
all_chunks = []

for filename in os.listdir('data'):
    if filename.endswith('.txt'):
        filepath = os.path.join('data', filename)
        print(f'Processing {filename}...')

        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        chunks = chunk_text(text, source=filename)
        all_chunks.extend(chunks)
        print(f'  → {len(chunks)} chunks')

# Save chunks to file
os.makedirs('chunks', exist_ok=True)
output_path = 'chunks/all_chunks.txt'

with open(output_path, 'w', encoding='utf-8') as f:
    for i, chunk in enumerate(all_chunks):
        f.write(f"CHUNK {i+1} | SOURCE: {chunk['source']} | TOKENS: {chunk['tokens']}\n")
        f.write(chunk['text'])
        f.write('\n\n---\n\n')

print(f'\nTotal chunks: {len(all_chunks)}')
print(f'Saved to {output_path}')

# Print 5 sample chunks for inspection
print('\n========== 5 SAMPLE CHUNKS ==========\n')
step = max(1, len(all_chunks) // 5)
for i in range(0, min(5, len(all_chunks))):
    chunk = all_chunks[i * step]
    print(f'CHUNK {i+1} | SOURCE: {chunk["source"]} | TOKENS: {chunk["tokens"]}')
    print(chunk['text'])
    print('\n---\n')