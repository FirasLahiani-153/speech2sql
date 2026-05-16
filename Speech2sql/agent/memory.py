class ConversationMemory:
    def __init__(self, max_turns=5):
        self.turns = []
        self.max_turns = max_turns

    def add_turn(self, arabic, english, sql, rows):
        self.turns.append({
            "arabic": arabic,
            "english": english,
            "sql": sql,
            "rows": rows
        })
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    def get_context(self):
        if not self.turns:
            return "No previous conversation."
        lines = []
        for i, turn in enumerate(self.turns, 1):
            lines.append(f"[Turn {i}]")
            if turn["arabic"]:
                lines.append(f"  User (Arabic) : {turn['arabic']}")
            lines.append(f"  User (English): {turn['english']}")
            lines.append(f"  SQL generated : {turn['sql']}")
            lines.append(f"  Rows returned : {turn['rows']}")
        return "\n".join(lines)

    def clear(self):
        self.turns = []

    def __len__(self):
        return len(self.turns)
