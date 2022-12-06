module.exports = {
  renderTypeSection: function (label, commits) {
    let text = `\n##** Changelog **\n`;

    commits.forEach((commit) => {
      text += `- ${commit.subject}\n`;
    });

    return text;
  },

  renderChangelog: function (release, changes) {
    return `<@&967698392870436874> New release ${release} is dropped! Check it out!\n\n` + changes;
  },
};
