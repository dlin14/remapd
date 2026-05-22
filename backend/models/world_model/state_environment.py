"""
StateEnvironment — reserved module for future RL environment work.

The current optimizer (`models/agent/rl_agent.py`) uses simulated annealing
over county-to-district assignments, which proved faster and more reliable
for the hackathon timeline.

A full Gymnasium-compatible environment would allow swapping in PPO or other
policy-gradient algorithms. The interface would look like:

    env = StateEnvironment(state_fips="06", n_districts=52)
    obs, info = env.reset()
    obs, reward, terminated, truncated, info = env.step(action)

Key design decisions for a future implementation:
- Observation space: per-county feature vectors (population, minority share,
  geographic centroid) + current district assignment.
- Action space: Discrete(n_counties) — reassign one county at a time.
- Reward: same weighted formula used in the current annealing optimizer
  (racial fairness, population equality, compactness, voting-rights proxy).
- Contiguity: enforce geographic adjacency constraints on each step.
"""
