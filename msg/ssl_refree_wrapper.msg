
# The UNIX timestamp when the packet was sent, in microseconds.
# Divide by 1,000,000 to get a time_t.
uint64 packet_timestamp

# The "coarse" stage of the game.
ssl_refree_stage stage

# The number of microseconds left in the stage.
# Becomes negative when a stage runs over its specified time.
int32 stage_time_left

# The "fine" states of play.
ssl_refree_command command

# Number of commands issued since startup.
# The ssl_referee.proto comments: (mod 2^32).
# This probably means that it wraps back to 0 when it overflows.
uint32 command_counter

# UNIX timestamp of when the command was issued, in microseconds.
# Value changes only when a new command gets issued, not on each packet.
uint64 command_timestamp

ssl_refree_teaminfo us
ssl_refree_teaminfo them


vector2D designated_position
