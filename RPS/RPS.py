# Standalone player function
import random
def player(prev_opponent_play, state={"opponent_history": []}):
    def update_history(prev_opponent_play):
        if prev_opponent_play:
            state["opponent_history"].append(prev_opponent_play)

    def build_markov_model(order):
        model = {}
        for i in range(len(state["opponent_history"]) - order):
            history = tuple(state["opponent_history"][i:i+order])
            next_play = state["opponent_history"][i+order]
            if history not in model:
                model[history] = {'R': 0, 'P': 0, 'S': 0}
            model[history][next_play] += 1
        return model

    def predict_play(order):
        if len(state["opponent_history"]) >= order:
            history = tuple(state["opponent_history"][-order:])
            if history in model:
                next_play = max(model[history], key=model[history].get)
                return {'R': 'P', 'P': 'S', 'S': 'R'}[next_play]

        # Fallback to a simpler strategy if there's not enough history
        last_play = state["opponent_history"][-1] if state["opponent_history"] else random.choice(['R', 'P', 'S'])
        return {'P': 'S', 'R': 'P', 'S': 'R'}[last_play]

    if prev_opponent_play == ' ':
        # Reset the history for a new opponent
        state["opponent_history"] = []
        return random.choice(['R', 'P', 'S']) 
      # Default play for the first move against a new opponent

    update_history(prev_opponent_play)

    # Build and update the Markov model with a higher order
    order =  5 # Experiment with different order values
    model = build_markov_model(order)

    # Predict the next play using the Markov model
    predicted_play = predict_play(order)

    # Introduce adaptability based on opponent behavior
    if state["opponent_history"].count(prev_opponent_play) > len(state["opponent_history"]) / 2:
        # If opponent frequently repeats a move, counter it
        return {'R': 'P', 'P': 'S', 'S': 'R'}[prev_opponent_play]

    return predicted_play

