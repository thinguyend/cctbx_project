#include <scitbx/array_family/boost_python/flex_wrapper.h>
#include <scitbx/array_family/boost_python/flex_pickle_single_buffered.h>
#include <boost/python/args.hpp>
#include <boost/python/overloads.hpp>
#include <boost/python/make_constructor.hpp>

namespace scitbx { namespace af { namespace boost_python {

namespace {

  template <typename UnsignedType>
  struct from_iselection
  {
    static
    flex<bool>::type*
    get(
      std::size_t size,
      af::const_ref<UnsignedType> const& iselection)
    {
      af::shared<bool> result(size, false);
      for(std::size_t i=0;i<iselection.size();i++) {
        SCITBX_ASSERT(iselection[i] < size);
        result[iselection[i]] = true;
      }
      return new flex<bool>::type(result, result.size());
    }
  };

  af::shared<int>
  as_int(af::const_ref<bool> const& self)
  {
    af::shared<int> result((af::reserve(self.size())));
    for(std::size_t i=0;i<self.size();i++) {
      result.push_back(self[i] ? 1 : 0);
    }
    return result;
  }

  af::shared<double>
  as_double(af::const_ref<bool> const& self)
  {
    af::shared<double> result((af::reserve(self.size())));
    for(std::size_t i=0;i<self.size();i++) {
      result.push_back(self[i] ? 1 : 0);
    }
    return result;
  }

  af::shared<std::size_t>
  iselection(
    af::const_ref<bool, flex_grid<> > const& a,
    bool test_value=true)
  {
    af::shared<std::size_t> result;
    for(std::size_t i=0;i<a.size();i++) {
      if (a[i] == test_value) result.push_back(i);
    }
    return result;
  }

  BOOST_PYTHON_FUNCTION_OVERLOADS(iselection_overloads, iselection, 1, 2)

  template <typename UnsignedType>
  struct union_core
  {
    union_core(
      boost::python::object const& iselection,
      af::ref<bool> result)
    :
      ok(false)
    {
      boost::python::extract<af::const_ref<UnsignedType> > proxy(iselection);
      if (proxy.check()) {
        ok = true;
        af::const_ref<UnsignedType> iselection = proxy();
        for(std::size_t i=0;i<iselection.size();i++) {
          SCITBX_ASSERT(iselection[i] < result.size());
          result[iselection[i]] = true;
        }
      }
    }

    bool ok;
  };

  af::shared<bool>
  union_(
    std::size_t size,
    boost::python::list const& iselections)
  {
    af::shared<bool> result(size, false);
    af::ref<bool> r = result.ref();
    std::size_t n_iselections = boost::python::len(iselections);
    for(std::size_t i=0;i<n_iselections;i++) {
      bool ok = union_core<unsigned>(iselections[i], r).ok;
      if (!ok && boost::python::type_info(typeid(af::const_ref<std::size_t>))
              != boost::python::type_info(typeid(af::const_ref<unsigned>))) {
        ok = union_core<std::size_t>(iselections[i], r).ok;
      }
      if (!ok) {
        throw error("iselections must be arrays of unsigned or size_t.");
      }
    }
    return result;
  }

  template <typename UnsignedType>
  struct intersection_core
  {
    intersection_core(
      boost::python::object const& iselection,
      af::ref<bool> result,
      af::ref<bool> tmp)
    :
      ok(false)
    {
      SCITBX_ASSERT(tmp.size() == result.size());
      boost::python::extract<af::const_ref<UnsignedType> > proxy(iselection);
      if (proxy.check()) {
        ok = true;
        af::const_ref<UnsignedType> iselection = proxy();
        for(std::size_t i=0;i<iselection.size();i++) {
          SCITBX_ASSERT(iselection[i] < result.size());
          tmp[iselection[i]] = true;
        }
        for(std::size_t i=0;i<result.size();i++) {
          if (tmp[i]) tmp[i] = false;
          else        result[i] = false;
        }
      }
    }

    bool ok;
  };

  af::shared<bool>
  intersection(
    std::size_t size,
    boost::python::list const& iselections)
  {
    af::shared<bool> result(size, true);
    af::shared<bool> tmp(size, false);
    af::ref<bool> r = result.ref();
    af::ref<bool> t = tmp.ref();
    std::size_t n_iselections = boost::python::len(iselections);
    for(std::size_t i=0;i<n_iselections;i++) {
      bool ok = intersection_core<unsigned>(iselections[i], r, t).ok;
      if (!ok && boost::python::type_info(typeid(af::const_ref<std::size_t>))
              != boost::python::type_info(typeid(af::const_ref<unsigned>))) {
        ok = intersection_core<std::size_t>(iselections[i], r, t).ok;
      }
      if (!ok) {
        throw error("iselections must be arrays of unsigned or size_t.");
      }
    }
    return result;
  }

  template <typename UnsignedType>
  af::shared<UnsignedType>
  filter_indices(
    af::const_ref<bool> const& self,
    af::const_ref<UnsignedType> const& indices)
  {
    af::shared<UnsignedType> result;
    for(std::size_t i=0;i<indices.size();i++) {
      SCITBX_ASSERT(indices[i] < self.size());
      if (self[indices[i]]) {
        result.append(indices[i]);
      }
    }
    return result;
  }

} // namespace <anonymous>

  void wrap_flex_bool()
  {
    using namespace boost::python;
    flex_wrapper<bool>::logical("bool", scope())
      .def_pickle(flex_pickle_single_buffered<bool>())
      .def("__init__", make_constructor(
        &from_iselection<unsigned>::get,
        default_call_policies(),
        (arg_("size"), arg_("iselection"))))
      .def("__init__", make_constructor(
        &from_iselection<std::size_t>::get,
        default_call_policies(),
        (arg_("size"), arg_("iselection"))))
      .def("as_int", as_int)
      .def("as_double", as_double)
      .def("iselection", iselection,
        iselection_overloads((arg_("self"), arg_("test_value")=true)))
      .def("filter_indices",
        (af::shared<std::size_t>(*)(
           af::const_ref<bool> const&,
           af::const_ref<std::size_t> const&)) filter_indices,
        (arg_("self"), arg_("indices")))
    ;
    def("union", union_, (arg_("size"), arg_("iselections")));
    def("intersection", intersection, (arg_("size"), arg_("iselections")));
  }

}}} // namespace scitbx::af::boost_python
