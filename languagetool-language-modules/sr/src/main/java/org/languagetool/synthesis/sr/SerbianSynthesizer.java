/* LanguageTool, a natural language style checker
 * Copyright (C) 2017 Daniel Naber (http://www.danielnaber.de)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
 * USA
 */
package org.languagetool.synthesis.sr;

import org.languagetool.synthesis.BaseSynthesizer;

/**
 * Serbian generic word form synthesizer
 *
 * @author Zoltan Csala
 * @since 4.0
 */
public class SerbianSynthesizer extends BaseSynthesizer {

  protected static final String DICTIONARY_PATH = "/sr/dictionary/";
  protected static final String TAGS_FILE_NAME = DICTIONARY_PATH + "serbian_synth_tags.txt";

  /**
   * @param resourceFileName The dictionary file name.
   * @param tagFileName      The name of a file containing all possible tags.
   */
<<<<<<< HEAD
  public SerbianSynthesizer(final String resourceFileName, final String tagFileName) {
=======
  public SerbianSynthesizer(String resourceFileName, String tagFileName) {
>>>>>>> e8f4ad8238abfb79fe729c777f07d0ad8a9caf25
    super(resourceFileName, tagFileName);
  }
}
