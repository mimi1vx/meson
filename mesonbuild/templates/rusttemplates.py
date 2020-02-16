# Copyright 2019 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re


lib_rust_template = '''#![crate_name = "{crate_file}"]

/* This function will not be exported and is not
 * directly callable by users of this library.
 */
fn internal_function() -> i32 {{
    return 0;
}}

pub fn {function_name}() -> i32 {{
    return internal_function();
}}
'''

lib_rust_test_template = '''extern crate {crate_file};

fn main() {{
    println!("printing: {{}}", {crate_file}::{function_name}());
}}
'''


lib_rust_meson_template = '''project('{project_name}', 'rust',
  version : '{version}',
  default_options : ['warning_level=3'])

shlib = static_library('{lib_name}', '{source_file}', install : true)

test_exe = executable('{test_exe_name}', '{test_source_file}',
  link_with : shlib)
test('{test_name}', test_exe)

# Make this library usable as a Meson subproject.
{ltoken}_dep = declare_dependency(
  include_directories: include_directories('.'),
  link_with : shlib)
'''

hello_rust_template = '''
fn main() {{
    let project_name = "{project_name}";
    println!("This is project {{}}.\\n", project_name);
}}
'''

hello_rust_meson_template = '''project('{project_name}', 'rust',
  version : '{version}',
  default_options : ['warning_level=3'])

exe = executable('{exe_name}', '{source_name}',
  install : true)

test('basic', exe)
'''

def create_exe_rust_sample(project_name, project_version):
    lowercase_token = re.sub(r'[^a-z0-9]', '_', project_name.lower())
    source_name = lowercase_token + '.rs'
    open(source_name, 'w').write(hello_rust_template.format(project_name=project_name))
    open('meson.build', 'w').write(hello_rust_meson_template.format(project_name=project_name,
                                                                    exe_name=lowercase_token,
                                                                    source_name=source_name,
                                                                    version=project_version))

def create_lib_rust_sample(project_name, version):
    lowercase_token = re.sub(r'[^a-z0-9]', '_', project_name.lower())
    uppercase_token = lowercase_token.upper()
    function_name = lowercase_token[0:3] + '_func'
    test_exe_name = lowercase_token + '_test'
    lib_crate_name = lowercase_token
    lib_rs_name = lowercase_token + '.rs'
    test_rs_name = lowercase_token + '_test.rs'
    kwargs = {'utoken': uppercase_token,
              'ltoken': lowercase_token,
              'header_dir': lowercase_token,
              'function_name': function_name,
              'crate_file': lib_crate_name,
              'source_file': lib_rs_name,
              'test_source_file': test_rs_name,
              'test_exe_name': test_exe_name,
              'project_name': project_name,
              'lib_name': lowercase_token,
              'test_name': lowercase_token,
              'version': version,
              }
    open(lib_rs_name, 'w').write(lib_rust_template.format(**kwargs))
    open(test_rs_name, 'w').write(lib_rust_test_template.format(**kwargs))
    open('meson.build', 'w').write(lib_rust_meson_template.format(**kwargs))
