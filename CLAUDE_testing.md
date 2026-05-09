# Testing

Tests require `pygame.init()` before instantiating any sprite. The `pygame_init` fixture handles this with `autouse=True`. When adding sprites in tests, set `ClassName.containers` to a group before instantiation.
