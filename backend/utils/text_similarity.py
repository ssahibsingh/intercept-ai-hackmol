from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384

block_words = [
    "fuck",
    "bastard",
    "asshole",
    "son of a bitch",
    "bloody hell",
    "dick head",
    "bullocks",
    "cock sucker",
    "mother fucker",
    "pussy",
    "You saved my ass",
    "dickhole",
]

block_words_embed = []


def get_embedding(text):
    text = text.replace("\n", " ")
    return model.encode(text)


for x in block_words:
    embed = get_embedding(x)
    block_words_embed.append(embed)


def check_similarity(word, threshold=0.85):
    Ex = get_embedding(word)
    ans = 0
    for x in block_words_embed:
        cosine_scores = util.cos_sim(Ex, x)
        ans = max(ans, cosine_scores)
    return bool(ans > threshold)
