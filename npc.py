class NPC:
    def __init__(self, emotion="neutral"):
        self.state = emotion
    
    def update_behavior(self, emotion):
        if emotion == "happy":
            self.state = "friendly"
        elif emotion == "angry":
            self.state = "defensive"
        elif emotion == "sad":
            self.state = "sympathetic"
        elif emotion == "surprise":
            self.state = "curious"
        else:
            self.state = "neutral"
    
    def interact(self):
        behaviours = { #This is a template for how the NPC may act once properly implemented. 
            "friendly": "NPC smiles and offers help.",
            "defensive": "NPC keeps distance and watches you cautiously.",
            "sympathetic": "NPC asks if you're okay and offers support.",
            "curious": "NPC leans in, interested in your reaction.",
            "neutral": "NPC nods and waits for your action."
        }
        print("NPC Behavior:", behaviours.get(self.state, "NPC is idle."))