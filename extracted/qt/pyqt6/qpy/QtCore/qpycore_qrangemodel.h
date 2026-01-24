// This is the interface support for QRangeModel.
//
// Copyright (c) 2026 Riverbank Computing Limited <info@riverbankcomputing.com>
// 
// This file is part of PyQt6.
// 
// This file may be used under the terms of the GNU General Public License
// version 3.0 as published by the Free Software Foundation and appearing in
// the file LICENSE included in the packaging of this file.  Please review the
// following information to ensure the GNU General Public License version 3.0
// requirements will be met: http://www.gnu.org/copyleft/gpl.html.
// 
// If you do not wish to use this file under the terms of the GPL version 3.0
// then you may purchase a commercial license.  For more information contact
// info@riverbankcomputing.com.
// 
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


#ifndef _QPYCORE_QRANGEMODEL_H
#define _QPYCORE_QRANGEMODEL_H

#include <Python.h>

#include <qglobal.h>

#if QT_VERSION >= 0x060a00

#include <qlist.h>
#include <qobject.h>
#include <qrangemodel.h>
#include <qvariant.h>


class sipQRangeModel;


// The abstract base for classes that wrap a Python object to be used as an
// appropriately configured range for use by QRangeModel.
class QPyAbstractRange : public QObject
{
    Q_OBJECT

public:
    QPyAbstractRange(PyObject *data, bool editable);
    virtual ~QPyAbstractRange();

    PyObject *data() const
    {
#if PY_VERSION_HEX >= 0x030a0000
        return Py_NewRef(m_data);
#else
        Py_INCREF(m_data);
        return m_data;
#endif
    }

    bool editable() const {return m_editable;}

    // This is internal.
    virtual sipQRangeModel *create(QObject *parent) = 0;

protected:
    // These are internal.
    static void raiseBadStructure();
    static bool populate1DFromList(QVariantList &range, PyObject *data);
    static bool populate1DFromSequence(QVariantList &range, PyObject *data);

private:
    PyObject *m_data;
    bool m_editable;
};


// A class that wraps a Python object to be used as an appropriately configured
// sequence range for use by QRangeModel.
class QPySequenceRange : public QPyAbstractRange
{
    Q_OBJECT

public:
    QPySequenceRange(PyObject *data, bool editable = false);

    // This is internal.
    sipQRangeModel *create(QObject *parent);

signals:
    void dataChanged(int index);

private slots:
    void handleDataChanged(const QModelIndex &tl, const QModelIndex &br);

private:
    QVariantList m_seq_range;

    static bool populateFromList(QVariantList &range, PyObject *data);
    static bool populateFromSequence(QVariantList &range, PyObject *data);
};


// A class that wraps a Python object to be used as an appropriately configured
// table range for use by QRangeModel.
class QPyTableRange : public QPyAbstractRange
{
    Q_OBJECT

public:
    QPyTableRange(PyObject *data, bool editable = false);

    // This is internal.
    sipQRangeModel *create(QObject *parent);

signals:
    void dataChanged(int row, int column);

private slots:
    void handleDataChanged(const QModelIndex &tl, const QModelIndex &br);

private:
    QList<QVariantList> m_table_range;

    bool populate(QList<QVariantList> &range, PyObject *data);
};

#endif

#endif
