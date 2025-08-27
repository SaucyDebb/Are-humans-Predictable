# What data are we using?
As stated in the introduction, the model is trained using the Lichess’s open database, which provides millions of chess games in PGN (Portable Game Notation) format.

# 📊 Does Lichess Game History Mostly Consist of High-Rated Players?
Nope — Lichess is open-source and widely used by players across the entire skill spectrum. Its database includes everything from casual blitz games to elite-level classical matches.

# 🧩 Player Types in Lichess Game History
| Player Type         | Characteristics                                                                 |
|---------------------|----------------------------------------------------------------------------------|
| Casual / Beginner   | Random or short games, often with blunders and non-standard openings            |
| Intermediate        | Some opening theory, basic tactics, inconsistent strategy                       |
| Advanced / High-rated | Strong adherence to theory, layered tactics, strategic depth, clean endgames  |

# 🔍 Game Types
- Bullet/blitz games with chaotic patterns  
- Classical games with textbook motifs  
- Training games and engine matches  
- Games with missing metadata (e.g., unrated or anonymous players)  

# 🧠 Data Used for Training
For effective pattern recognition, filtering by **rating** and **time control** is key. Different rating bands offer distinct advantages when training models or analyzing gameplay.

# 🎯 Rating-Based Filtering
| Rating Band     | Training Value                                                             |
|-----------------|----------------------------------------------------------------------------|
| Above 1800 Elo  | More reliable for strategic and endgame patterns                           |
| Below 1200 Elo  | Great for studying common mistakes and missed tactics                      |

# Why?
- High-rated games tend to reflect deliberate decision-making and textbook motifs, making them ideal for modeling strategic depth.  
- Low-rated games, on the other hand, are rich in unintentional patterns—perfect for training error detection and tactical awareness.

# 🏷️ For Best Tagging Efficiency
To ensure accurate and scalable pattern recognition, we apply different tagging styles based on the nature of each group.

| Group     | Tagging Style      | Why?                                                                 |
|-----------|--------------------|----------------------------------------------------------------------|
| Opening   | Grouped            | Defined by first 10–15 moves, often includes transpositions          |
| Tactics   | Individual         | Occur at specific moves, easy to detect and label                    |
| Strategy  | Grouped + Flags    | Emergent over time, but flag key moments (e.g., pawn push, imbalance)|
| Endgame   | Individual         | Recognizable positions (Lucena, Philidor, etc.)                      |

# 🔄 Tagging Pipeline Overview
- **Preprocess PGN**: Extract moves, metadata, rating  
- **Opening Classifier**: Match first 10 moves to ECO codes  
- **Tactic Detector**: Use engine evaluation swings + piece positions  
- **Strategic Theme Flags**: Identify pawn structures, imbalances, key transitions  
- **Endgame Recognizer**: Match known positions or endgame motifs  