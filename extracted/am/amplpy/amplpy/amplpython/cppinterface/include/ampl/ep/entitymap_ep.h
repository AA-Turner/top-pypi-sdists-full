#ifndef AMPL_ENTITYMAP_EP_H
#define AMPL_ENTITYMAP_EP_H

#include <map>
#include <string>

#include "ampl/ep/declarations.h"
#include "ampl/ep/error_information.h"
#include "ampl/ep/errorinfo_ep.h"

namespace ampl {
class Variable;
class Constraint;
class Objective;
class Parameter;
class Set;
class Table;

namespace internal {

template <class EntityClass>
struct EntityMapRefPointer {
  typedef typename std::map<std::string, EntityClass *>::const_iterator
      iterator_type;
  std::size_t count_;
  iterator_type it_;
  EntityMapRefPointer(size_t count, const iterator_type &it)
      : count_(count), it_(it) {}
};

template <class EntityClass>
class EntityMap;
class Variable;
class Objective;
class Parameter;
class Set;
class Constraint;
class Table;

extern "C" {
AMPLAPI Variable *AMPL_EntityMap_Variable_get(EntityMap<Variable> *impl,
                                              const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Variable_size(EntityMap<Variable> *impl);
AMPLAPI EntityMapRefPointer<Variable> *AMPL_EntityMap_iterator_Variable_begin(
    EntityMap<Variable> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Variable> *AMPL_EntityMap_iterator_Variable_end(
    EntityMap<Variable> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Variable> *AMPL_EntityMap_iterator_Variable_find(
    EntityMap<Variable> *impl, const char *name, ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Variable_equal(
    EntityMapRefPointer<Variable> *it1, EntityMapRefPointer<Variable> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Variable_delete(
    EntityMapRefPointer<Variable> *it);
AMPLAPI void AMPL_EntityMap_iterator_Variable_increment(
    EntityMapRefPointer<Variable> *it, ErrorInformation *errorInfo);
AMPLAPI Variable *AMPL_EntityMap_iterator_Variable_second(
    EntityMapRefPointer<Variable> *it, ErrorInformation *errorInfo);

AMPLAPI Objective *AMPL_EntityMap_Objective_get(EntityMap<Objective> *impl,
                                                const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Objective_size(EntityMap<Objective> *impl);
AMPLAPI EntityMapRefPointer<Objective> *AMPL_EntityMap_iterator_Objective_begin(
    EntityMap<Objective> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Objective> *AMPL_EntityMap_iterator_Objective_end(
    EntityMap<Objective> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Objective> *AMPL_EntityMap_iterator_Objective_find(
    EntityMap<Objective> *impl, const char *name, ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Objective_equal(
    EntityMapRefPointer<Objective> *it1, EntityMapRefPointer<Objective> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Objective_delete(
    EntityMapRefPointer<Objective> *it);
AMPLAPI void AMPL_EntityMap_iterator_Objective_increment(
    EntityMapRefPointer<Objective> *it, ErrorInformation *errorInfo);
AMPLAPI Objective *AMPL_EntityMap_iterator_Objective_second(
    EntityMapRefPointer<Objective> *it, ErrorInformation *errorInfo);

AMPLAPI Set *AMPL_EntityMap_Set_get(EntityMap<Set> *impl, const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Set_size(EntityMap<Set> *impl);
AMPLAPI EntityMapRefPointer<Set> *AMPL_EntityMap_iterator_Set_begin(
    EntityMap<Set> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Set> *AMPL_EntityMap_iterator_Set_end(
    EntityMap<Set> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Set> *AMPL_EntityMap_iterator_Set_find(
    EntityMap<Set> *impl, const char *name, ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Set_equal(EntityMapRefPointer<Set> *it1,
                                               EntityMapRefPointer<Set> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Set_delete(EntityMapRefPointer<Set> *it);
AMPLAPI void AMPL_EntityMap_iterator_Set_increment(EntityMapRefPointer<Set> *it,
                                                   ErrorInformation *errorInfo);
AMPLAPI Set *AMPL_EntityMap_iterator_Set_second(EntityMapRefPointer<Set> *it,
                                                ErrorInformation *errorInfo);

AMPLAPI Parameter *AMPL_EntityMap_Parameter_get(EntityMap<Parameter> *impl,
                                                const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Parameter_size(EntityMap<Parameter> *impl);
AMPLAPI EntityMapRefPointer<Parameter> *AMPL_EntityMap_iterator_Parameter_begin(
    EntityMap<Parameter> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Parameter> *AMPL_EntityMap_iterator_Parameter_end(
    EntityMap<Parameter> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Parameter> *AMPL_EntityMap_iterator_Parameter_find(
    EntityMap<Parameter> *impl, const char *name, ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Parameter_equal(
    EntityMapRefPointer<Parameter> *it1, EntityMapRefPointer<Parameter> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Parameter_delete(
    EntityMapRefPointer<Parameter> *it);
AMPLAPI void AMPL_EntityMap_iterator_Parameter_increment(
    EntityMapRefPointer<Parameter> *it, ErrorInformation *errorInfo);
AMPLAPI Parameter *AMPL_EntityMap_iterator_Parameter_second(
    EntityMapRefPointer<Parameter> *it, ErrorInformation *errorInfo);

AMPLAPI Table *AMPL_EntityMap_Table_get(EntityMap<Table> *impl,
                                        const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Table_size(EntityMap<Table> *impl);
AMPLAPI EntityMapRefPointer<Table> *AMPL_EntityMap_iterator_Table_begin(
    EntityMap<Table> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Table> *AMPL_EntityMap_iterator_Table_end(
    EntityMap<Table> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Table> *AMPL_EntityMap_iterator_Table_find(
    EntityMap<Table> *impl, const char *name, ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Table_equal(
    EntityMapRefPointer<Table> *it1, EntityMapRefPointer<Table> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Table_delete(
    EntityMapRefPointer<Table> *it);
AMPLAPI void AMPL_EntityMap_iterator_Table_increment(
    EntityMapRefPointer<Table> *it, ErrorInformation *errorInfo);
AMPLAPI Table *AMPL_EntityMap_iterator_Table_second(
    EntityMapRefPointer<Table> *it, ErrorInformation *errorInfo);

AMPLAPI Constraint *AMPL_EntityMap_Constraint_get(EntityMap<Constraint> *impl,
                                                  const char *name);
AMPLAPI std::size_t AMPL_EntityMap_Constraint_size(EntityMap<Constraint> *impl);
AMPLAPI EntityMapRefPointer<Constraint>
    *AMPL_EntityMap_iterator_Constraint_begin(EntityMap<Constraint> *impl,
                                              ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Constraint> *AMPL_EntityMap_iterator_Constraint_end(
    EntityMap<Constraint> *impl, ErrorInformation *errorInfo);
AMPLAPI EntityMapRefPointer<Constraint>
    *AMPL_EntityMap_iterator_Constraint_find(EntityMap<Constraint> *impl,
                                             const char *name,
                                             ErrorInformation *errorInfo);
AMPLAPI bool AMPL_EntityMap_iterator_Constraint_equal(
    EntityMapRefPointer<Constraint> *it1, EntityMapRefPointer<Constraint> *it2);
AMPLAPI void AMPL_EntityMap_iterator_Constraint_delete(
    EntityMapRefPointer<Constraint> *it);
AMPLAPI void AMPL_EntityMap_iterator_Constraint_increment(
    EntityMapRefPointer<Constraint> *it, ErrorInformation *errorInfo);
AMPLAPI Constraint *AMPL_EntityMap_iterator_Constraint_second(
    EntityMapRefPointer<Constraint> *it, ErrorInformation *errorInfo);
}  // C Linkage

template <typename EntityPrivate>
struct EntityFunctions;

template <>
struct EntityFunctions<ampl::Variable> {
  static Variable *getMap(EntityMap<Variable> *impl, const char *name) {
    return AMPL_EntityMap_Variable_get(impl, name);
  }

  static std::size_t size(EntityMap<Variable> *impl) {
    return AMPL_EntityMap_Variable_size(impl);
  }

  static internal::EntityMapRefPointer<Variable> *begin(
      EntityMap<Variable> *impl) {
    return AMPL_EntityMap_iterator_Variable_begin(impl, ErrorInfo());
  }
  static internal::EntityMapRefPointer<Variable> *end(
      EntityMap<Variable> *impl) {
    return AMPL_EntityMap_iterator_Variable_end(impl, ErrorInfo());
  }
  static internal::EntityMapRefPointer<Variable> *find(
      EntityMap<Variable> *impl, const char *name) {
    return AMPL_EntityMap_iterator_Variable_find(impl, name, ErrorInfo());
  }
  static bool equal(internal::EntityMapRefPointer<Variable> *it1,
                    internal::EntityMapRefPointer<Variable> *it2) {
    return AMPL_EntityMap_iterator_Variable_equal(it1, it2);
  }
  static void delete_iterator(internal::EntityMapRefPointer<Variable> *it) {
    AMPL_EntityMap_iterator_Variable_delete(it);
  }
  static void increment(internal::EntityMapRefPointer<Variable> *it) {
    AMPL_EntityMap_iterator_Variable_increment(it, ErrorInfo());
  }
  static Variable *second(internal::EntityMapRefPointer<Variable> *it) {
    return AMPL_EntityMap_iterator_Variable_second(it, ErrorInfo());
  }
};

template <>
struct EntityFunctions<ampl::Constraint> {
  static Constraint *getMap(EntityMap<Constraint> *impl, const char *name) {
    return AMPL_EntityMap_Constraint_get(impl, name);
  }
  static std::size_t size(EntityMap<Constraint> *impl) {
    return AMPL_EntityMap_Constraint_size(impl);
  }
  static EntityMapRefPointer<Constraint> *begin(EntityMap<Constraint> *impl) {
    return AMPL_EntityMap_iterator_Constraint_begin(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Constraint> *end(EntityMap<Constraint> *impl) {
    return AMPL_EntityMap_iterator_Constraint_end(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Constraint> *find(EntityMap<Constraint> *impl,
                                               const char *name) {
    return AMPL_EntityMap_iterator_Constraint_find(impl, name, ErrorInfo());
  }
  static bool equal(EntityMapRefPointer<Constraint> *it1,
                    EntityMapRefPointer<Constraint> *it2) {
    return AMPL_EntityMap_iterator_Constraint_equal(it1, it2);
  }
  static void delete_iterator(EntityMapRefPointer<Constraint> *it) {
    AMPL_EntityMap_iterator_Constraint_delete(it);
  }
  static void increment(EntityMapRefPointer<Constraint> *it) {
    AMPL_EntityMap_iterator_Constraint_increment(it, ErrorInfo());
  }
  static Constraint *second(internal::EntityMapRefPointer<Constraint> *it) {
    return AMPL_EntityMap_iterator_Constraint_second(it, ErrorInfo());
  }
};

template <>
struct EntityFunctions<ampl::Parameter> {
  static Parameter *getMap(EntityMap<Parameter> *impl, const char *name) {
    return AMPL_EntityMap_Parameter_get(impl, name);
  }
  static std::size_t size(EntityMap<Parameter> *impl) {
    return AMPL_EntityMap_Parameter_size(impl);
  }
  static EntityMapRefPointer<Parameter> *begin(EntityMap<Parameter> *impl) {
    return AMPL_EntityMap_iterator_Parameter_begin(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Parameter> *end(EntityMap<Parameter> *impl) {
    return AMPL_EntityMap_iterator_Parameter_end(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Parameter> *find(EntityMap<Parameter> *impl,
                                              const char *name) {
    return AMPL_EntityMap_iterator_Parameter_find(impl, name, ErrorInfo());
  }
  static bool equal(EntityMapRefPointer<Parameter> *it1,
                    EntityMapRefPointer<Parameter> *it2) {
    return AMPL_EntityMap_iterator_Parameter_equal(it1, it2);
  }
  static void delete_iterator(EntityMapRefPointer<Parameter> *it) {
    AMPL_EntityMap_iterator_Parameter_delete(it);
  }
  static void increment(EntityMapRefPointer<Parameter> *it) {
    AMPL_EntityMap_iterator_Parameter_increment(it, ErrorInfo());
  }
  static Parameter *second(internal::EntityMapRefPointer<Parameter> *it) {
    return AMPL_EntityMap_iterator_Parameter_second(it, ErrorInfo());
  }
};

template <>
struct EntityFunctions<ampl::Set> {
  static Set *getMap(EntityMap<Set> *impl, const char *name) {
    return AMPL_EntityMap_Set_get(impl, name);
  }
  static std::size_t size(EntityMap<Set> *impl) {
    return AMPL_EntityMap_Set_size(impl);
  }
  static EntityMapRefPointer<Set> *begin(EntityMap<Set> *impl) {
    return AMPL_EntityMap_iterator_Set_begin(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Set> *end(EntityMap<Set> *impl) {
    return AMPL_EntityMap_iterator_Set_end(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Set> *find(EntityMap<Set> *impl,
                                        const char *name) {
    return AMPL_EntityMap_iterator_Set_find(impl, name, ErrorInfo());
  }
  static bool equal(EntityMapRefPointer<Set> *it1,
                    EntityMapRefPointer<Set> *it2) {
    return AMPL_EntityMap_iterator_Set_equal(it1, it2);
  }
  static void delete_iterator(EntityMapRefPointer<Set> *it) {
    AMPL_EntityMap_iterator_Set_delete(it);
  }
  static void increment(EntityMapRefPointer<Set> *it) {
    AMPL_EntityMap_iterator_Set_increment(it, ErrorInfo());
  }
  static Set *second(internal::EntityMapRefPointer<Set> *it) {
    return AMPL_EntityMap_iterator_Set_second(it, ErrorInfo());
  }
};

template <>
struct EntityFunctions<ampl::Objective> {
  static Objective *getMap(EntityMap<Objective> *impl, const char *name) {
    return AMPL_EntityMap_Objective_get(impl, name);
  }
  static std::size_t size(EntityMap<Objective> *impl) {
    return AMPL_EntityMap_Objective_size(impl);
  }
  static EntityMapRefPointer<Objective> *begin(EntityMap<Objective> *impl) {
    return AMPL_EntityMap_iterator_Objective_begin(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Objective> *end(EntityMap<Objective> *impl) {
    return AMPL_EntityMap_iterator_Objective_end(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Objective> *find(EntityMap<Objective> *impl,
                                              const char *name) {
    return AMPL_EntityMap_iterator_Objective_find(impl, name, ErrorInfo());
  }
  static bool equal(EntityMapRefPointer<Objective> *it1,
                    EntityMapRefPointer<Objective> *it2) {
    return AMPL_EntityMap_iterator_Objective_equal(it1, it2);
  }
  static void delete_iterator(EntityMapRefPointer<Objective> *it) {
    AMPL_EntityMap_iterator_Objective_delete(it);
  }
  static void increment(EntityMapRefPointer<Objective> *it) {
    AMPL_EntityMap_iterator_Objective_increment(it, ErrorInfo());
  }
  static Objective *second(internal::EntityMapRefPointer<Objective> *it) {
    return AMPL_EntityMap_iterator_Objective_second(it, ErrorInfo());
  }
};

template <>
struct EntityFunctions<ampl::Table> {
  static Table *getMap(EntityMap<Table> *impl, const char *name) {
    return AMPL_EntityMap_Table_get(impl, name);
  }
  static std::size_t size(EntityMap<Table> *impl) {
    return AMPL_EntityMap_Table_size(impl);
  }
  static EntityMapRefPointer<Table> *begin(EntityMap<Table> *impl) {
    return AMPL_EntityMap_iterator_Table_begin(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Table> *end(EntityMap<Table> *impl) {
    return AMPL_EntityMap_iterator_Table_end(impl, ErrorInfo());
  }
  static EntityMapRefPointer<Table> *find(EntityMap<Table> *impl,
                                          const char *name) {
    return AMPL_EntityMap_iterator_Table_find(impl, name, ErrorInfo());
  }
  static bool equal(EntityMapRefPointer<Table> *it1,
                    EntityMapRefPointer<Table> *it2) {
    return AMPL_EntityMap_iterator_Table_equal(it1, it2);
  }
  static void delete_iterator(EntityMapRefPointer<Table> *it) {
    AMPL_EntityMap_iterator_Table_delete(it);
  }
  static void increment(EntityMapRefPointer<Table> *it) {
    AMPL_EntityMap_iterator_Table_increment(it, ErrorInfo());
  }
  static Table *second(internal::EntityMapRefPointer<Table> *it) {
    return AMPL_EntityMap_iterator_Table_second(it, ErrorInfo());
  }
};
}  // namespace internal
}  // namespace ampl

#endif  // AMPL_ENTITYMAP_EP_H
