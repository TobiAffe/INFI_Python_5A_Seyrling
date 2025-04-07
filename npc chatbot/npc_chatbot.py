import ollama
import threading
import pygame

class NPCBot:
    def __init__(self, pos: pygame.Vector2, range_radius=120):
        self.pos = pos
        self.range = range_radius
        self.messages = [
            {"role": "system", "content": "Du bist Eldrin, ein weiser Magier. Du sprichst in Rätseln und gibst kryptische Hinweise."}
        ]
        self.latest_riddle = "..."
        self.generating = False
        self.was_player_near = False
        self.show_text = False

    def start_riddle_thread(self):
        if not self.generating:
            self.generating = True
            thread = threading.Thread(target=self._generate_riddle)
            thread.daemon = True
            thread.start()

    def _generate_riddle(self):
        try:
            self.messages.append({"role": "user", "content": "Sprich ein neues Rätsel."})
            response = ollama.chat(model="gemma:2b", messages=self.messages)
            riddle = response["message"]["content"]
            self.messages.append({"role": "assistant", "content": riddle})
            self.latest_riddle = riddle
        except Exception as e:
            self.latest_riddle = f"[Fehler: {e}]"
        self.generating = False

    def update(self, player_pos: pygame.Vector2):
        distance = player_pos.distance_to(self.pos)
        in_range = distance < self.range

        if in_range and not self.was_player_near:
            self.start_riddle_thread()
            self.show_text = True
        elif not in_range and self.was_player_near:
            self.show_text = False

        self.was_player_near = in_range

    def draw_text(self, surface, font, max_width=200):
        if self.show_text:
            text = self.latest_riddle if not self.generating else "... denkt nach ..."
            self._render_multiline(surface, font, text, self.pos.x - 60, self.pos.y - 60, font, (0, 0, 0), max_width)

    def _render_multiline(self, surface, font, text, x, y, font_obj, color, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font_obj.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        for i, line in enumerate(lines):
            line_surface = font_obj.render(line, True, color)
            surface.blit(line_surface, (x, y + i * font_obj.get_linesize()))
