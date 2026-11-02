using System;
using System.Collections.Generic;
using System.Reflection;

namespace Python.Runtime
{
    public class BindingOptions
    {
        private bool _SuppressDocs = false;
        private bool _SuppressOverloads = false;
        private bool _AllowExplicitInterfaceImplementation = false;
        private bool _Pep8Aliases = false;

        //[ModuleProperty]
        public bool SuppressDocs
        {
            get { return _SuppressDocs; }
            set { _SuppressDocs = value; }
        }

        //[ModuleProperty]
        public bool SuppressOverloads
        {
            get { return _SuppressOverloads; }
            set { _SuppressOverloads = value; }
        }

        public bool AllowExplicitInterfaceImplementation
        {
            get { return _AllowExplicitInterfaceImplementation; }
            set { _AllowExplicitInterfaceImplementation = value; }
        }

        public bool Pep8Aliases
        {
            get { return _Pep8Aliases; }
            set { _Pep8Aliases = value; }
        }
    }

    public class BindingManager
    {
        static IDictionary<Type, BindingOptions> _typeOverrides = new Dictionary<Type, BindingOptions>();
        static IDictionary<Assembly, BindingOptions> _assemblyOverrides = new Dictionary<Assembly, BindingOptions>();
        static BindingOptions _defaultBindingOptions = new BindingOptions();

        public static BindingOptions GetBindingOptions(Type type)
        {
            if (_typeOverrides.ContainsKey(type))
            {
                return _typeOverrides[type];
            }

            if (_assemblyOverrides.ContainsKey(type.Assembly))
            {
                return _assemblyOverrides[type.Assembly];
            }
            return _defaultBindingOptions;
        }

        public static BindingOptions DefaultBindingOptions => _defaultBindingOptions;

        public static void SetBindingOptions(Type type, BindingOptions options)
        {
            _typeOverrides[type] = options;
        }

        public static void SetBindingOptions(Assembly assembly, BindingOptions options)
        {
            _assemblyOverrides[assembly] = options;
        }

        public static void Clear()
        {
            _typeOverrides.Clear();
            _assemblyOverrides.Clear();
        }
    }
}
