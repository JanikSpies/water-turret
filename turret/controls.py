STEP_DEG = 5

# Codes from cv2.waitKeyEx: macOS and Linux report arrow keys differently.
LEFT_KEYS = {63234, 65361, ord("a")}
RIGHT_KEYS = {63235, 65363, ord("d")}
UP_KEYS = {63232, 65362, ord("w")}
DOWN_KEYS = {63233, 65364, ord("s")}
QUIT_KEYS = {ord("q")}


def key_to_nudge(key: int) -> tuple[int, int] | None:
    """Maps a pressed key to a (d_pan, d_tilt) step, or None if it isn't a move key."""
    if key in LEFT_KEYS:
        return -STEP_DEG, 0
    if key in RIGHT_KEYS:
        return STEP_DEG, 0
    if key in UP_KEYS:
        return 0, -STEP_DEG
    if key in DOWN_KEYS:
        return 0, STEP_DEG
    return None
