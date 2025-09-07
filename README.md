# Are-humans-Predictable
A model that is **Learning People**, Not Just the Game.

Unlike advanced engines built to crush opponents with perfect play, this model is trained to understand human decision‑making patterns — the common moves, predictable choices, and mistakes we make under pressure.
Its goal isn’t to “win at all costs,” but to reveal why we make certain moves, so players can learn from their own tendencies and improve.
It’s chess as a mirror — not a machine.

Inspired by Friday, Tony Stark’s AI assistant in Avengers: Civil War, this project explores predictive modeling through the lens of strategic gameplay. From a scene, where Friday analyzes Captain America's fighting patterns and feeds Tony countermeasures in real time. That concept sparked the initial idea: an AI that could anticipate and counter human behavior.

# Pivoting from Combat to Chess
Due to hardware limitations and resource constraints, the project shifted from real-time combat prediction to a more computationally feasible domain: chess. Despite being turn-based, chess offers a rich landscape of strategic depth, pattern recognition, and psychological nuance—perfect for testing predictive capabilities.

# Why Chess?
Chess, while less physically demanding, still embodies the core challenge—anticipating complex strategies and countering them effectively. The model is trained on high-level gameplay, learning from grandmasters and strategic patterns. Its goal is to predict the opponent’s most probable moves, combinations, or strategies, and respond with optimal counterplay.

Conceptually, it mirrors what Friday achieved: real-time analysis and strategic adaptation based on behavioral patterns.

# Project Goals
- Train a model on high-level chess games and strategic patterns
- Predict the opponent’s most likely next move, combination, or strategy
- Generate counter-strategies in real time, mimicking the reactive intelligence of Friday

# So, What Data Is the Model Trained On
The model is trained using Lichess’s open database, which provides millions of chess games in PGN (Portable Game Notation) format.

# What are the Key Elements?
While PGN files contain a wide range of metadata, for this project we focus on the elements most relevant to strategic prediction:
- Board state at each move (implicitly derived from move history)
- Move taken (in algebraic notation)
- Game result (win/loss/draw)
- Player ratings (to filter for high-level games)
- Opening name (optional, for clustering strategies)

# So, What Do We Actually Use?
Despite the richness of PGN, the model only needs two key ingredients:
- Current board state
- Move taken from that state

And by grouping identical board states across games, we can analyze:
- Which moves were most commonly chosen
- Their associated win rates
- Strategic tendencies based on player rating or opening type
This allows the model to build a probability-weighted map of likely responses and their effectiveness

# But Is It Really That Simple?
Not quite. While this approach mimics human decision-making, modern models like AlphaZero go further. They don’t just learn from human games—they play against themselves, exploring new strategies through trial and error.
They learn things like:
- “When I prioritize king safety, I tend to win.”
- “When I push g4 in this pawn structure, I gain attacking chances.”

This kind of reinforcement learning allows the model to discover strategic value beyond human intuition. It’s not just copying—it’s learning.
Kind of like us, really. We play, we lose, we adapt. The difference?
The model processes thousands of games in seconds, refining its instincts faster than our brains ever could.

# So, What Will This Project Achieve?
At its core, Are-Humans-Predictable is a step toward understanding and anticipating human decision-making through strategic modeling. By starting with chess, the project builds a foundation for:
- Predictive insight: Learning how humans respond to specific board states and what patterns emerge across skill levels
- Counter-strategy generation: Offering real-time responses that aren’t just reactive—but strategically proactive
- Behavioral modeling: Exploring how AI can interpret and adapt to human tendencies, even in constrained environments

# Long-Term Vision
While the current scope focuses on chess, the underlying architecture could be extended to other domains—fighting games, negotiation simulations, or even emotionally intelligent agents that anticipate conversational dynamics.
The end goal?

To create an AI that doesn’t just calculate—it understands. One that can learn from patterns, adapt to new contexts, and offer meaningful counterplay in any strategic setting.
Whether it’s a pawn push or a punch feint, the dream is the same:
Anticipate. Adapt. Evolve.
