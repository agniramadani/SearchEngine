import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.document import TextField, StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
from java.nio.file import Paths
import csv

# Initialize Lucene
lucene.initVM()

# Directory for the index
index_dir = MMapDirectory(Paths.get("index"))

# Analyzer and configuration
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)

# Create an IndexWriter
index_writer = IndexWriter(index_dir, config)

# Read the CSV file and index the data
csv_file = 'songs.csv'
try:
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        unique_titles = set()  # Track unique titles for debug
        
        for row in reader:
            if row['title'] not in unique_titles:
                unique_titles.add(row['title'])
                doc = Document()
                doc.add(TextField("title", row['title'], Field.Store.YES))
                doc.add(TextField("artist", row['artist'], Field.Store.YES))
                doc.add(TextField("genre", row['genre'], Field.Store.YES))
                doc.add(StringField("year", row['year'], Field.Store.YES))
                index_writer.addDocument(doc)
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

# Commit and close the writer
index_writer.commit()
index_writer.close()
