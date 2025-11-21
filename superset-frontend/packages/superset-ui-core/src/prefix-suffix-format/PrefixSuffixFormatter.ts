/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file for additional
 * information regarding copyright ownership.  The ASF licenses this file to you
 * under the Apache License, Version 2.0 (the "License"); you may not use this file
 * except in compliance with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed
 * under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations under the License.
 */

import { ExtensibleFunction } from '../models';
import { ValueFormatter } from '../types';

interface PrefixSuffixFormatterConfig {
  formatter: ValueFormatter;
  prefix?: string;
  suffix?: string;
}

interface PrefixSuffixFormatter {
  (value: number | null | undefined): string;
}

class PrefixSuffixFormatter extends ExtensibleFunction {
  formatter: ValueFormatter;

  prefix: string;

  suffix: string;

  constructor(config: PrefixSuffixFormatterConfig) {
    super((value: number) => this.format(value));
    this.formatter = config.formatter;
    this.prefix = config.prefix || '';
    this.suffix = config.suffix || '';
  }

  format(value: number): string {
    const formattedValue = this.formatter.format(value);
    return `${this.prefix}${formattedValue}${this.suffix}`;
  }
}

export default PrefixSuffixFormatter;
