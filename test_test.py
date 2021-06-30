'''
fig = plt.figure(figsize=(17,8))
ax1 = plt.subplot(221)
X1 = list(dens_df.time)
Y1 = list(dens_df.intensity)
ax1.scatter(range(len(Y1)), Y1, c='b')
ax1.set_title('Intensity')
ax1.set_xlim(0, len(Y1) - 1)
ax1.set_xticks(range(len(Y1)))
ax1.set_xticklabels(X1)

ax2 = plt.subplot(222)
X2 = X1
Y2 = list(dens_df.velocity)
ax2.scatter(range(len(Y2)), Y2, c='r')
ax2.set_title('Velocity')
ax2.set_xlim(0, len(Y2) - 1)
ax2.set_xticks(range(len(Y2)))
ax2.set_xticklabels(X2)

ax3 = plt.subplot(212)
X3 = X1
Y3 = list(dens_df.density)
ax3.scatter(range(len(Y3)), Y3, c='g')
ax3.set_title('Density')
ax3.set_xlim(0, len(Y3) - 1)
ax3.set_xticks(range(len(Y3)))
ax3.set_xticklabels(X3)
'''