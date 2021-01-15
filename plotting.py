import matplotlib.colors as mcolors
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np

def gradient_fill(x, y, fill_color=None, ax=None, min_alpha=0.0, fill_alpha=1.0, **kwargs):
    """
    Plot a line with a linear alpha gradient filled beneath it.

    Parameters
    ----------
    x, y : array-like
        The data values of the line.
    fill_color : a matplotlib color specifier (string, tuple) or None
        The color for the fill. If None, the color of the line will be used.
    ax : a matplotlib Axes instance
        The axes to plot on. If None, the current pyplot axes will be used.
    Additional arguments are passed on to matplotlib's ``plot`` function.

    Returns
    -------
    line : a Line2D instance
        The line plotted.
    im : an AxesImage instance
        The transparent gradient clipped to just the area beneath the curve.

    This function is taken from the stack overflow article here:
    https://stackoverflow.com/questions/29321835/is-it-possible-to-get-color-gradients-under-curve-in-matplotlib
    """

    if ax is None:
        ax = plt.gca()

    line, = ax.plot(x, y, **kwargs)
    if fill_color is None:
        fill_color = line.get_color()

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha
    fill_alpha = fill_alpha*alpha
    min_alpha = (0.0 if min_alpha is None else min_alpha)*fill_alpha

    num_segments = 100
    
    z = np.empty((num_segments, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:,:,:3] = rgb
    z[:,:,-1] = np.linspace(min_alpha, alpha, num_segments)[:,None]

    xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = np.column_stack([x, y])
    xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
    clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)

    return line, im

def gradient_fill_about_level(x, y, y_level, fill_color=None, ax=None, min_alpha=0.0, fill_alpha=1.0, **kwargs):
    """
    Plot a line with a linear alpha gradient filled beneath it.

    Parameters
    ----------
    x, y : array-like
        The data values of the line.
    fill_color : a matplotlib color specifier (string, tuple) or None
        The color for the fill. If None, the color of the line will be used.
    ax : a matplotlib Axes instance
        The axes to plot on. If None, the current pyplot axes will be used.
    Additional arguments are passed on to matplotlib's ``plot`` function.

    Returns
    -------
    line : a Line2D instance
        The line plotted.
    im : an AxesImage instance
        The transparent gradient clipped to just the area beneath the curve.

    This function is taken from the stack overflow article here:
    https://stackoverflow.com/questions/29321835/is-it-possible-to-get-color-gradients-under-curve-in-matplotlib
    """

    if ax is None:
        ax = plt.gca()

    # Plot line
    line, = ax.plot(x, y, **kwargs)
    if fill_color is None:
        fill_color = line.get_color()

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha
    fill_alpha = fill_alpha*alpha
    min_alpha = (0.0 if min_alpha is None else min_alpha)*fill_alpha

    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()

    num_segments = 100

    z = np.empty((num_segments, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:,:,:3] = rgb
    if y_level > ymax:
        z[:,:,-1] = np.linspace(fill_alpha, fill_alpha*((y_level-ymax)/(y_level-ymin)), num_segments)[:,None]
    elif y_level < ymin:
        z[:,:,-1] = np.linspace(fill_alpha*((ymin-y_level)/(ymax-y_level)), fill_alpha, num_segments)[:,None]
    else:
        up_wid = ymax-y_level
        low_wid = y_level-ymin
        max_wid = max(up_wid, low_wid)
        wid = ymax-ymin
        low_frac = low_wid/wid
        num_low = int(num_segments*low_frac)
        num_high = num_segments-num_low
        zs = np.concatenate([
            np.linspace(fill_alpha*(low_wid/max_wid), min_alpha, num_low),
            np.linspace(min_alpha, fill_alpha*(up_wid/max_wid), num_high)
        ])
        z[:,:,-1] = zs[:,None]

    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = np.column_stack([x, y])
    if y_level > ymax:
        #xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
        pass
    elif y_level < ymin:
        #xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
        pass
    else:
        xy = np.vstack([[xmin, y_level], xy, [xmax, y_level], [xmin, y_level]])
    clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)

    return line, im
