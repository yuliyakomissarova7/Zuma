from modules.path_generator import PathGenerator


class TestPathGenerator:
    def setup_class(self):
        self.path = (PathGenerator(0))
        self.path.points = [(0, 6), (6, 6), (6, 12)]

    def test_get_ball_position(self):
        expected_result = [(0, 6), (2, 6), (4, 6), (6, 6), (6, 8), (6, 10), (6, 12)]
        self.path.get_ball_positions()
        actual = self.path.ball_positions
        actual_result = []
        for vector in actual:
            actual_result.append((int(vector[0]), int(vector[1])))
        assert actual_result == expected_result
