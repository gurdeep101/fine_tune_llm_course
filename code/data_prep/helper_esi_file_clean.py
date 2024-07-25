import re

def figure_text_clean(text_file):
    pattern = re.compile(re.escape(text_file) + r".{100}")
    return pattern.sub(" ", text_file)

def group_adjacent_rectangles(rectangles, distance_threshold):
    """
    Group a list of rectangles into adjacent sets if the coordinates overlap or the distance between the rectangles
    is less than a specified value.
    
    Parameters:
    rectangles (list of tuples): A list of tuples where each tuple contains four integers (x1, y1, x2, y2) representing the coordinates of the bottom-left and top-right corners of a rectangle.
    distance_threshold (int): The maximum distance between rectangles to consider them as adjacent.
    
    Returns:
    list of lists of tuples: A list where each element is a list of tuples representing a group of adjacent rectangles.
    """
    def rectangles_overlap_or_close(rect1, rect2, threshold):
        # Check if rectangles overlap
        if not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3]):
            return True
        # Check if rectangles are within the distance threshold
        if (abs(rect1[2] - rect2[0]) <= threshold or abs(rect1[0] - rect2[2]) <= threshold) and \
           (rect1[1] <= rect2[3] and rect1[3] >= rect2[1]):
            return True
        if (abs(rect1[3] - rect2[1]) <= threshold or abs(rect1[1] - rect2[3]) <= threshold) and \
           (rect1[0] <= rect2[2] and rect1[2] >= rect2[0]):
            return True
        return False

    def find_adjacent_group(rect, remaining_rects, threshold):
        group = [rect]
        to_check = [rect]
        while to_check:
            current = to_check.pop()
            for other in remaining_rects[:]:
                if rectangles_overlap_or_close(current, other, threshold):
                    group.append(other)
                    to_check.append(other)
                    remaining_rects.remove(other)
        return group

    remaining_rects = rectangles[:]
    groups = []
    while remaining_rects:
        rect = remaining_rects.pop(0)
        group = find_adjacent_group(rect, remaining_rects, distance_threshold)
        groups.append(group)
    
    return groups