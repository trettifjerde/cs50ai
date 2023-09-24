import os
import random
import re
import sys
from bisect import bisect_left

DAMPING = 0.85
SAMPLES = 10000
ACCURACY = 0.001


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition = dict()
    # if page contains links
    if corpus[page]:
    	# assign probability to the links on the page
    	p_pagelink = 1 / len(corpus[page]) * damping_factor
    	for pagename in corpus[page]:
    		transition[pagename] = p_pagelink
    	# assign random visit probability to every page in the corpus 
    	p_randomlink = (1 - damping_factor) / len(corpus)
    	for pagename in corpus:
    		transition[pagename] = transition.get(pagename, 0) + p_randomlink
    # otherwise every page in the corpus has an equal chance of being visited
    else:
    	p_randomlink = 1 / len(corpus)
    	for pagename in corpus:
    		transition[pagename] = p_randomlink

    return transition


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page = random.choice(list(corpus))
    pagerank = {page: 1}
    counter = 0

    while counter < n:
    	transition = transition_model(corpus, page, damping_factor)
    	pages, cumprobs = [], []
    	total = 0

    	for k, v in transition.items():
    		pages.append(k)
    		total += v
    		cumprobs.append(total)

    	r = random.random()
    	page = pages[bisect_left(cumprobs, r)]

    	pagerank[page] = pagerank.get(page, 0) + 1
    	counter += 1

    for page in pagerank:
    	pagerank[page] = pagerank[page] / n

    return pagerank


def incoming_pages(corpus, link):
	"""
	Returns a dict of all the pages containing the specified link
	with the total number of links on the page as values.
	"""
	pages = dict()
	for page in corpus:
		if link in corpus[page]:
			pages[page] = len(corpus[page])
	return pages

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pagerank = {page: 1/len(corpus) for page in corpus}
    # Make a copy of the corpus
    # where all the linkless pages
    # lead to every other page in the corpus.
    corpus_adjusted = corpus.copy()
    for page in corpus_adjusted:
    	if not corpus_adjusted[page]:
    		corpus_adjusted[page] = set((page for page in corpus))

    random_visit = (1 - damping_factor) / len(corpus)

    while True:
    	convergent = True
    	for page in corpus_adjusted:
    		new_rank = sum(pagerank[incoming_page] / numlinks
    			for incoming_page, numlinks
    			in incoming_pages(corpus_adjusted, page).items()
    		)
    		new_rank = new_rank * damping_factor + random_visit
    		if abs(pagerank[page] - new_rank) > ACCURACY:
    			convergent = False
    		pagerank[page] = new_rank
    	if convergent:
    		break
    return pagerank
    
if __name__ == "__main__":
    main()
