# encoding: utf-8

"""
Axis-related chart objects.
"""

from __future__ import absolute_import, print_function, unicode_literals

from ..enum.chart import XL_TICK_LABEL_POSITION, XL_TICK_MARK
from ..oxml.ns import qn
from ..text.text import Font
from ..util import lazyproperty


class _BaseAxis(object):
    """
    Base class for chart axis objects. All axis objects share these
    properties.
    """
    def __init__(self, xAx_elm):
        super(_BaseAxis, self).__init__()
        self._element = xAx_elm

    @property
    def has_major_gridlines(self):
        """
        Read/write boolean value specifying whether this axis has gridlines
        at its major tick mark locations. Assigning |True| to this property
        causes major gridlines to be displayed. Assigning |False| causes them
        to be removed.
        """
        if self._element.majorGridlines is None:
            return False
        return True

    @has_major_gridlines.setter
    def has_major_gridlines(self, value):
        if bool(value) is True:
            self._element.get_or_add_majorGridlines()
        else:
            self._element._remove_majorGridlines()

    @property
    def has_minor_gridlines(self):
        """
        Read/write boolean value specifying whether this axis has gridlines
        at its minor tick mark locations. Assigning |True| to this property
        causes minor gridlines to be displayed. Assigning |False| causes them
        to be removed.
        """
        if self._element.minorGridlines is None:
            return False
        return True

    @has_minor_gridlines.setter
    def has_minor_gridlines(self, value):
        if bool(value) is True:
            self._element.get_or_add_minorGridlines()
        else:
            self._element._remove_minorGridlines()

    @property
    def major_tick_mark(self):
        """
        Read/write :ref:`XlTickMark` value specifying the type of major tick
        mark to display on this axis.
        """
        majorTickMark = self._element.majorTickMark
        if majorTickMark is None:
            return XL_TICK_MARK.CROSS
        return majorTickMark.val

    @major_tick_mark.setter
    def major_tick_mark(self, value):
        self._element._remove_majorTickMark()
        if value is XL_TICK_MARK.CROSS:
            return
        self._element._add_majorTickMark(val=value)

    @property
    def maximum_scale(self):
        """
        Read/write float value specifying the upper limit of the value range
        for this axis, the number at the top or right of the vertical or
        horizontal value scale, respectively. The value |None| indicates the
        upper limit should be determined automatically based on the range of
        data point values associated with the axis.
        """
        return self._element.scaling.maximum

    @maximum_scale.setter
    def maximum_scale(self, value):
        scaling = self._element.scaling
        scaling.maximum = value

    @property
    def minimum_scale(self):
        """
        Read/write float value specifying lower limit of value range, the
        number at the bottom or left of the value scale. |None| if no minimum
        scale has been set. The value |None| indicates the lower limit should
        be determined automatically based on the range of data point values
        associated with the axis.
        """
        return self._element.scaling.minimum

    @minimum_scale.setter
    def minimum_scale(self, value):
        scaling = self._element.scaling
        scaling.minimum = value

    @property
    def minor_tick_mark(self):
        """
        Read/write :ref:`XlTickMark` value specifying the type of minor tick
        mark for this axis.
        """
        minorTickMark = self._element.minorTickMark
        if minorTickMark is None:
            return XL_TICK_MARK.CROSS
        return minorTickMark.val

    @minor_tick_mark.setter
    def minor_tick_mark(self, value):
        self._element._remove_minorTickMark()
        if value is XL_TICK_MARK.CROSS:
            return
        self._element._add_minorTickMark(val=value)

    @lazyproperty
    def tick_labels(self):
        """
        The |TickLabels| instance providing access to axis tick label
        formatting properties. Tick labels are the numbers appearing on
        a value axis or the category names appearing on a category axis.
        """
        return TickLabels(self._element)

    @property
    def tick_label_position(self):
        """
        Read/write :ref:`XlTickLabelPosition` value specifying where the tick
        labels for this axis should appear.
        """
        tickLblPos = self._element.tickLblPos
        if tickLblPos is None:
            return XL_TICK_LABEL_POSITION.NEXT_TO_AXIS
        if tickLblPos.val is None:
            return XL_TICK_LABEL_POSITION.NEXT_TO_AXIS
        return tickLblPos.val

    @tick_label_position.setter
    def tick_label_position(self, value):
        tickLblPos = self._element.get_or_add_tickLblPos()
        tickLblPos.val = value

    @property
    def visible(self):
        """
        Read/write. |True| if axis is visible, |False| otherwise.
        """
        delete = self._element.delete
        if delete is None:
            return False
        return False if delete.val else True

    @visible.setter
    def visible(self, value):
        if value not in (True, False):
            raise ValueError(
                "assigned value must be True or False, got: %s" % value
            )
        delete = self._element.get_or_add_delete()
        delete.val = not value


class CategoryAxis(_BaseAxis):
    """
    A category axis of a chart.
    """


class TickLabels(object):
    """
    A service class providing access to formatting of axis tick mark labels.
    """
    def __init__(self, xAx_elm):
        super(TickLabels, self).__init__()
        self._element = xAx_elm

    @lazyproperty
    def font(self):
        """
        The |Font| object that provides access to the text properties for
        these tick labels, such as bold, italic, etc.
        """
        defRPr = self._element.defRPr
        font = Font(defRPr)
        return font

    @property
    def number_format(self):
        """
        Read/write string (e.g. "$#,##0.00") specifying the format for the
        numbers on this axis. The syntax for these strings is the same as it
        appears in the PowerPoint or Excel UI. Returns 'General' if no number
        format has been set. Note that this format string has no effect on
        rendered tick labels when :meth:`number_format_is_linked` is |True|.
        Assigning a format string to this property automatically sets
        :meth:`number_format_is_linked` to |False|.
        """
        numFmt = self._element.numFmt
        if numFmt is None:
            return 'General'
        return numFmt.formatCode

    @number_format.setter
    def number_format(self, value):
        numFmt = self._element.get_or_add_numFmt()
        numFmt.formatCode = value
        self.number_format_is_linked = False

    @property
    def number_format_is_linked(self):
        """
        Read/write boolean specifying whether number formatting should be
        taken from the source spreadsheet rather than the value of
        :meth:`number_format`.
        """
        numFmt = self._element.numFmt
        if numFmt is None:
            return False
        souceLinked = numFmt.sourceLinked
        if souceLinked is None:
            return True
        return numFmt.sourceLinked

    @number_format_is_linked.setter
    def number_format_is_linked(self, value):
        numFmt = self._element.get_or_add_numFmt()
        numFmt.sourceLinked = value

    @property
    def offset(self):
        """
        Read/write int value in range 0-1000 specifying the spacing between
        the tick mark labels and the axis as a percentange of the default
        value. 100 if no label offset setting is present.
        """
        lblOffset = self._element.lblOffset
        if lblOffset is None:
            return 100
        return lblOffset.val

    @offset.setter
    def offset(self, value):
        if self._element.tag != qn('c:catAx'):
            raise ValueError('only a category axis has an offset')
        self._element._remove_lblOffset()
        if value == 100:
            return
        lblOffset = self._element._add_lblOffset()
        lblOffset.val = value


class ValueAxis(_BaseAxis):
    """
    A value axis of a chart.
    """
    @property
    def major_unit(self):
        """
        The float number of units between major tick marks on this value
        axis. |None| corresponds to the 'Auto' setting in the UI, and
        specifies the value should be calculated by PowerPoint based on the
        underlying chart data.
        """
        majorUnit = self._element.majorUnit
        if majorUnit is None:
            return None
        return majorUnit.val

    @major_unit.setter
    def major_unit(self, value):
        self._element._remove_majorUnit()
        if value is None:
            return
        self._element._add_majorUnit(val=value)

    @property
    def minor_unit(self):
        """
        The float number of units between minor tick marks on this value
        axis. |None| corresponds to the 'Auto' setting in the UI, and
        specifies the value should be calculated by PowerPoint based on the
        underlying chart data.
        """
        minorUnit = self._element.minorUnit
        if minorUnit is None:
            return None
        return minorUnit.val

    @minor_unit.setter
    def minor_unit(self, value):
        self._element._remove_minorUnit()
        if value is None:
            return
        self._element._add_minorUnit(val=value)
