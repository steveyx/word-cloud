from rectpack import newPacker

"""
single bin pack - 2 dimension 
"""


def bin_pack_2d(word_rectangles, xlim=0.8, ylim=1, ratio=10000, rotation=True):
    packer = newPacker(rotation=rotation)

    # Add the rectangles to packing queue
    _scaled_rects = []
    for i, r in enumerate(word_rectangles):
        _w, _h = int(r[0]*ratio), int(r[1]*ratio)
        _scaled_rects.append((_w, _h))
        packer.add_rect(_w, _h, rid=i)

    # Add one bin only
    packer.add_bin(int(xlim*ratio), int(ylim*ratio))

    # Start packing
    packer.pack()

    _packed_rects = packer.rect_list()
    _results = [{"x": x, "y": y, "w": w, "h": h, "b": b, "rid": rid} for b, x, y, w, h, rid in _packed_rects]
    _all_rects = set(range(len(word_rectangles)))
    _unpack_rects = list(_all_rects.difference(set([_r["rid"] for _r in _results])))
    for _r in _results:
        _r["vertical"] = 0 if _scaled_rects[_r["rid"]][0] == _r["w"] else 1
    return _results, _unpack_rects


if __name__ == "__main__":

    rectangles = [(100, 30), (40, 60), (30, 30), (70, 70), (100, 50), (30, 30), (30, 20, 5), (150, 180, 2)]
    packed, unpacked = bin_pack_2d(rectangles, xlim=80, ylim=450, ratio=1)
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    for rect in packed:
        x = rect["x"]
        y = rect["y"]
        w = rect["w"]
        h = rect["h"]
        ax.add_patch(Rectangle((x, y), w, h, fc='red', ec='g', lw=1))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 450)
    plt.show()
