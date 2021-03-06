/* *****************************************************
   THIS IS AN AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
   *****************************************************

   Generated by:
     scitbx.generate_error_h
 */

/*! \file
    Declarations and macros for exception handling.
 */

#ifndef IOTBX_ERROR_H
#define IOTBX_ERROR_H

#include <scitbx/error_utils.h>

#define IOTBX_CHECK_POINT \
  std::cout << __FILE__ << "(" << __LINE__ << ")" << std::endl << std::flush
#define IOTBX_CHECK_POINT_MSG(msg) \
  std::cout << msg << " @ " __FILE__ << "(" << __LINE__ << ")" << std::endl << std::flush
#define IOTBX_EXAMINE(A) \
  std::cout << "variable " << #A << ": " << A << std::endl << std::flush

//! Common iotbx namespace.
namespace iotbx {

  //! All iotbx exceptions are derived from this class.
  class error : public ::scitbx::error_base<error>
  {
    public:

      //! General iotbx error message.
      explicit
      error(std::string const& msg) throw()
        : ::scitbx::error_base<error>("iotbx", msg)
      {}

      //! Error message with file name and line number.
      /*! Used by the macros below.
       */
      error(const char* file, long line, std::string const& msg = "",
            bool internal = true) throw()
        : ::scitbx::error_base<error>("iotbx", file, line, msg, internal)
      {}
  };

  //! Special class for "Index out of range." exceptions.
  /*! These exceptions are propagated to Python as IndexError.
   */
  class error_index : public error
  {
    public:
      //! Default constructor. The message may be customized.
      explicit
      error_index(std::string const& msg = "Index out of range.") throw()
        : error(msg)
      {}
  };

} // namespace iotbx

//! For throwing an error exception with file name, line number, and message.
#define IOTBX_ERROR(msg) \
  SCITBX_ERROR_UTILS_REPORT(iotbx::error, msg)
//! For throwing an "Internal Error" exception.
#define IOTBX_INTERNAL_ERROR() \
  SCITBX_ERROR_UTILS_REPORT_INTERNAL(iotbx::error)
//! For throwing a "Not implemented" exception.
#define IOTBX_NOT_IMPLEMENTED() \
  SCITBX_ERROR_UTILS_REPORT_NOT_IMPLEMENTED(iotbx::error)

//! Custom iotbx assertion.
#define IOTBX_ASSERT(assertion) \
  SCITBX_ERROR_UTILS_ASSERT(iotbx::error, IOTBX_ASSERT, assertion)

#endif // IOTBX_ERROR_H
