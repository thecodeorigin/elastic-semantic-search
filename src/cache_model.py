from utils.vectorize import Vectorize

if __name__ == "__main__":
  print("Loading model into system cache...")
  Vectorize(sentences=["hehe"]).handle()
  print("Model loaded successfully!")
