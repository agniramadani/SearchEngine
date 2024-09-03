import lucene
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher, FuzzyQuery
from org.apache.lucene.index import DirectoryReader, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
from java.nio.file import Paths
from org.apache.lucene.search import TermQuery
from org.apache.lucene.index import Term

# Initialize Lucene
lucene.initVM()

# Directory for the index
index_dir = MMapDirectory(Paths.get("index"))

# Analyzer and configuration
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)

# Function to search the index
def search_index(query_string):
    try:
        # Open the index
        reader = DirectoryReader.open(index_dir)
        searcher = IndexSearcher(reader)
        parser = QueryParser("title", analyzer)
        
        # Parse the query
        query = parser.parse(query_string)
        hits = searcher.search(query, 10).scoreDocs
        
        # Collect results
        results = []
        for hit in hits:
            doc = searcher.doc(hit.doc)
            results.append({
                "title": doc.get("title"),
                "artist": doc.get("artist"),
                "genre": doc.get("genre"),
                "year": doc.get("year"),
            })
        
        # Close the reader
        reader.close()
        
        return results
    
    except Exception as e:
        print(f"An error occurred while searching the index: {e}")
        return []

# Function to suggest alternatives
def suggest_alternatives(query_string, max_suggestions=5):
    try:
        # Open the index
        reader = DirectoryReader.open(index_dir)
        searcher = IndexSearcher(reader)
        
        # Prepare the fuzzy query
        term = Term("title", query_string)
        fuzzy_query = FuzzyQuery(term, 2)
        suggestions = searcher.search(fuzzy_query, max_suggestions).scoreDocs
        
        # Collect suggestions
        results = []
        for hit in suggestions:
            doc = searcher.doc(hit.doc)
            results.append(doc.get("title"))
        
        # Close the reader
        reader.close()
        
        return results
    
    except Exception as e:
        print(f"An error occurred while suggesting alternatives: {e}")
        return []

# Example search
if __name__ == "__main__":

    # Search for the song by the title
    query_string = input('Search for a song: ')
    results = search_index(query_string)

    if not results:
        # If no results, suggest alternatives
        suggestions = suggest_alternatives(query_string)
        if suggestions:
            print("No results found. Did you mean:")
            for suggestion in suggestions:
                print(suggestion)
        else:
            print("No suggestions available.")
    else:
        for result in results:
            print(result)
